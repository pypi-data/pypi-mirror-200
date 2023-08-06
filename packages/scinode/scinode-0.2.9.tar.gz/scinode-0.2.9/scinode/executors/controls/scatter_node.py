from scinode.core.executor import Executor


class ScinodeScatter(Executor):
    """Scatter nodes executor"""

    def run(self):
        """
        0) Find all subtrees created by this node, and delete them
        1) Find all children nodes after the scatter node
        2) Create a new nodetree nt1
        3) build all children node inside new nodetree nt1
        4) use REF node
        5) launch the nodetree
        """
        print("Run for scatter {}".format(self.name))
        self.prepare()
        self.new_nodetree()
        self.set_gather_state()

    def prepare(self):
        from scinode.orm.db_nodetree import DBNodeTree

        self.delete_sub_nodetree()
        if isinstance(self.kwargs["Input"], dict):
            labels = self.kwargs["Input"].keys()
        else:
            labels = range(len(self.kwargs["Input"]))
        self.labels = labels
        print("  Scatter labels: {}".format(self.labels))
        # nodetree data
        self.nt = DBNodeTree(uuid=self.dbdata["metadata"]["nodetree_uuid"])
        self.copy_nodes = set(self.nt.record["connectivity"]["child_node"][self.name])

    def delete_sub_nodetree(self):
        """Delete nodetrees which are scattered from this node."""
        from scinode.database.nodetree import NodetreeClient

        # Find all subtrees created by this node, and delete them
        client = NodetreeClient()
        query = {"metadata.scatter_node": self.uuid}
        client.delete(query)

    def update_scatter_node(self, nt, label):
        """Create ref nodes for the missing nodes.
        Check the missing input nodes
        1) if the input node is scatter node, make a copy node, update the results.
        """
        from scinode.utils.node import serialize_item
        from scinode.utils.db import replace_one
        from scinode.database.client import scinodedb

        node = nt.nodes[self.name]
        print("    set the input socket for the nodes connect to the scatter node")
        data = node.dbdata["outputs"][0]
        data["value"] = self.kwargs["Input"][label]
        # print(data)
        replace_one(serialize_item(data), scinodedb["data"])
        print(f"Node {self.name} is a COPY node.")
        node.update_db_keys(
            {
                "metadata.node_type": "COPY",
                "state": "FINISHED",
                "action": "NONE",
            }
        )
        # add label for all children nodes
        node.update_db_keys({"metadata.scattered_label": str(label)})

    def new_nodetree(self):
        """Copy nodes to new nodetree"""
        for label in self.labels:
            # add new nodetree
            name = "{}_{}".format(self.nt.name, label)
            print(
                "    Copy {} nodes to new nodetree: {}, .".format(
                    name, len(self.copy_nodes)
                )
            )
            nt = self.nt.copy(
                name,
                self.copy_nodes,
                is_child=True,
                scatter_node=self.uuid,
                scattered_label=label,
                add_missing_node=True,
                miss_node_type="REF",
                miss_node_other_type=[self.name],
            )
            self.update_scatter_node(nt, label)
            nt.update_db_keys({f"nodes.{self.name}.node_type": "COPY"})
            nt.update_db_keys({f"nodes.{self.name}.state": "FINISHED"})
            #
            nt.launch()

    def set_gather_state(self):
        from scinode.database.db import scinodedb
        from scinode.engine.send_to_queue import send_message_to_queue
        from scinode.engine.config import broker_queue_name

        scatter = {}
        for label in self.labels:
            scatter[str(label)] = "CREATED"
        # all the children nodes should not run, instead the action should be gather.
        for name in self.copy_nodes:
            print(f"    Set Node {name} state to SCATTERED.")
            msg = f"{self.nodetree_uuid},node,{name}:state:SCATTERED"
            send_message_to_queue(broker_queue_name, msg)
            #
            print(f"    Add new key: scatter for Node {name}.")
            newvalues = {"$set": {f"nodes.{name}.scatter": scatter}}
            query = {"uuid": self.nt.uuid}
            scinodedb["nodetree"].update_one(query, newvalues)
        return (None,)
