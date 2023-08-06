from scinode.core.executor import Executor


class ScinodeUpdate(Executor):
    """Out the properties

    Args:
        BaseNode (_type_): _description_
    """

    def run(self):
        """
        1) Find all children nodes before the gather node
        3) Gather input socket data
        """
        from scinode.orm.db_nodetree import DBNodeTree
        from scinode.orm.db_node import DBNode
        from scinode.utils.db import replace_one
        from scinode.utils.node import serialize_item
        from scinode.database.client import scinodedb

        dbdata = self.dbdata
        print(
            "    Run for Update node, count: {}".format(
                self.dbdata["metadata"]["counter"]
            )
        )
        # nodetree data
        update_node = DBNode(uuid=dbdata["uuid"])
        nt = DBNodeTree(uuid=dbdata["metadata"]["nodetree_uuid"])
        inputs = dbdata["inputs"]
        non_from_nodes = []
        for link in inputs[1]["links"]:
            non_from_nodes.append(link["from_node"])
        # because we skip the daemon to set the state
        # we have to update the result manully here
        data = self.dbdata["outputs"][0]
        print("   Counter: {}".format(dbdata["metadata"]["counter"]))
        if dbdata["metadata"]["counter"] > 0:
            # reset all nodes and launch
            nt.reset_node(dbdata["name"], launch=True)
            data["value"] = self.kwargs["Update"]
            # print("    results: ", results)
            this_results = (self.kwargs["Update"],)
        else:
            data["value"] = self.kwargs["Input"]
            this_results = (self.kwargs["Input"],)
        # print("  Save results: ", results)
        replace_one(serialize_item(data), scinodedb["data"])
        update_node.update_db_keys(
            {"metadata.counter": dbdata["metadata"]["counter"] + 1}
        )
        return this_results
