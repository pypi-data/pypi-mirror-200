"""
"""
from scinode.core import DBItem
from scinode.core.db_node import DBNode
from scinode.engine.config import broker_queue_name
from scinode.engine.send_to_queue import send_message_to_queue
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def skip_ref_node(func):
    def wrapper(self, name, **kwargs):
        if self.record["nodes"][name]["node_type"] == "REF":
            raise Exception("Can not change state of a reference node")
        return func(self, name, **kwargs)

    return wrapper


class DBNodeTree(DBItem):
    """DBNodeTree Class.
    Nodetree with the data from the database.

    uuid: str
        uuid of the nodetree.

    Example:

    >>> # load nodetree data from database
    >>> nodetree = DBNodeTree(uuid=uuid)
    >>> nodetree.reset_node("add1")
    """

    db_name: str = "nodetree"

    def __init__(self, uuid=None) -> None:
        """_summary_

        Args:
            uuid (_type_, optional): _description_. Defaults to None.
            dbdata (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]
        self.daemon_name = self.record["metadata"]["daemon_name"]

    def update_nodetree_state(self, state, action):
        self.update_db_keys({"state": state, "action": action})

    def launch(self):
        """Launch nodetree."""
        from scinode.engine.send_to_queue import launch_nodetree
        from scinode.engine.config import broker_queue_name

        launch_nodetree(broker_queue_name, self.uuid)

    @classmethod
    def save(self, ntdata):
        """Save nodetree to database."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.debug("save_to_db: {}".format(ntdata["name"]))
        ntdata["state"] = "CREATED"
        lnt = LaunchNodeTree(ntdata)
        lnt.save()

    def edit_from_yaml(self, filename=None, string=None):
        from scinode.utils import load_yaml
        from scinode.utils.nodetree import get_nt_full_data

        new_data = load_yaml(filename=filename, string=string)
        ntdata = get_nt_full_data({"uuid": self.uuid})
        for ndata in new_data["nodes"]:
            ntdata["nodes"][ndata["name"]] = DBNode.update_from_dict(ndata)
        self.save(ntdata)

    def edit_node_from_yaml(self, uuid, filename=None, string=None):
        """Edit node from yaml file.

        Args:
            uuid (str): uuid the node be edited.
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            node: _description_
        """
        from scinode.utils import load_yaml
        from scinode.utils.nodetree import get_nt_full_data

        ndata = load_yaml(filename=filename, string=string)
        ndata = DBNode.update_from_dict(ndata)
        ntdata = get_nt_full_data({"uuid": self.uuid})
        ntdata["nodes"][ndata["name"]] = ndata
        self.save(ntdata)

    def set_node_property(self, name, data):
        """Edit node from yaml file.

        Args:
            uuid (str): uuid the node be edited.
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            node: _description_
        """
        from scinode.utils.nodetree import get_nt_full_data
        from scinode.utils.node import get_node_data

        query = {"uuid": self.record["nodes"][name]["uuid"]}
        ndata = get_node_data(query, {})
        # properties
        for name, p in data.items():
            ndata["properties"][name]["value"] = p
        # results
        ntdata = get_nt_full_data({"uuid": self.uuid})
        # print("ndata: ", ndata)
        ntdata["nodes"][ndata["name"]] = ndata
        # pprint(ntdata)
        self.save(ntdata)

    @property
    def dbdata_nodes(self):
        """Fetch node data from database
        1) node belongs to this nodetree
        2) reference node used in this nodetree

        Returns:
            dict: node data from database
        """
        from scinode.database.client import db_node

        query = {"metadata.nodetree_uuid": self.dbdata["uuid"]}
        project = {"_id": 0, "uuid": 1, "name": 1, "state": 1, "action": 1}
        datas = list(db_node.find(query, project))
        dbdata_nodes = {data["name"]: data for data in datas}
        # find the ref nodes
        ref_nodes = [
            node["name"]
            for node in self.record["nodes"].values()
            if node["node_type"] == "REF"
        ]
        # populate the ref nodes
        for name in ref_nodes:
            query = {"uuid": self.record["nodes"][name]["uuid"]}
            data = db_node.find_one(query, project)
            dbdata_nodes[name] = data

        return dbdata_nodes

    def cancel(self):
        dbdata_nodes = self.dbdata_nodes
        for name, dbdata in dbdata_nodes.items():
            node = DBNode(dbdata)
            node.update_db_keys({"action": "CANCEL"})
        self.action = "NONE"

    def copy(
        self,
        nodetree_name,
        namelists=None,
        is_child=False,
        scatter_node=None,
        scattered_label="",
        add_missing_node=True,
        miss_node_type="REF",
        miss_node_other_type=[],
    ):
        """Copy a nodetree and insert it into the database.

        Args:
            nodetree_name (str): name of the new nodetree
            namelists (list): names of the nodes that
                used to build this nodetree.
            add_missing_node: add_missing_node
        How to handle the missing input nodes?
        - reference ndoe
        - copy
        - none

        Returns:
            DBNodeTree: an instance of DBNodeTree class
        """
        import uuid

        print("namelists: ", namelists)
        record = self.db.find_one({"uuid": self.uuid}, {"_id": 0})
        # change name and uuid
        record["name"] = nodetree_name
        record["uuid"] = str(uuid.uuid1())
        record["state"] = "CREATED"
        record["action"] = "NONE"
        # scatter subnodetree
        if is_child:
            record["metadata"]["parent"] = self.uuid
            record["metadata"]["scatter_node"] = scatter_node
            record["metadata"]["scattered_label"] = scattered_label
            is_scattered_node = True
        else:
            is_scattered_node = False
        #
        record_nodes = record["nodes"]
        record["nodes"] = {}
        # copy all nodes
        # remove all nodes include other nodes not in namelists
        node_datas = {}
        if namelists is None:
            namelists = record_nodes.keys()
        for name in namelists:
            ndata = record_nodes[name]
            node = DBNode(uuid=ndata["uuid"])
            ndata = node.copy(
                name=ndata["name"],
                nodetree_uuid=record["uuid"],
                is_scattered_node=is_scattered_node,
                scattered_label=scattered_label,
            )
            node_datas[name] = ndata
        # find missing input nodes
        if add_missing_node:
            missing_nodes = self.find_missing_input_nodes(namelists)
            print("missing_nodes: ", missing_nodes)
            for name in missing_nodes:
                is_ref = True if miss_node_type == "REF" else False
                if name in miss_node_other_type:
                    is_ref = not is_ref
                ndata = record_nodes[name]
                node = DBNode(uuid=ndata["uuid"])
                ndata = node.copy(
                    name=ndata["name"],
                    nodetree_uuid=record["uuid"],
                    is_scattered_node=is_scattered_node,
                    is_ref=is_ref,
                )
                node_datas[name] = ndata
        #
        record["nodes"] = node_datas
        # remove all link include other nodes not in node_groups
        namelists = record["nodes"].keys()
        links = []
        for link in record["links"]:
            if link["from_node"] in namelists and link["to_node"] in namelists:
                links.append(link)
        record["links"] = links
        for name, node in record["nodes"].items():
            # print(name, node["inputs"])
            for input in node["inputs"]:
                links = []
                for link in input["links"]:
                    if link["from_node"] in namelists and link["to_node"] in namelists:
                        # update socket uuid
                        from_node = record["nodes"][link["from_node"]]
                        from_socket = [
                            s
                            for s in from_node["outputs"]
                            if s["name"] == link["from_socket"]
                        ][0]
                        link["from_socket_uuid"] = from_socket["uuid"]
                        links.append(link)
                input["links"] = links
            for output in node["outputs"]:
                links = []
                for link in output["links"]:
                    if link["from_node"] in namelists and link["to_node"] in namelists:
                        to_node = record["nodes"][link["to_node"]]
                        to_socket = [
                            s
                            for s in to_node["inputs"]
                            if s["name"] == link["to_socket"]
                        ][0]
                        link["to_socket_uuid"] = to_socket["uuid"]
                        links.append(link)
                output["links"] = links
        # print("record: ", record)
        self.save(record)
        return self.__class__(uuid=record["uuid"])

    def find_missing_input_nodes(self, namelists):
        """Find the missing input nodes"""
        missing_nodes = []
        input_nodes = []
        for node in namelists:
            inputs = self.record["connectivity"]["input_node"][node]
            for socket, input in inputs.items():
                input_nodes.extend(input)
        missing_nodes = set(input_nodes) - set(namelists)
        print("missing_nodes: ", missing_nodes)
        return missing_nodes

    @property
    def nodes(self):
        return self.get_nodes()

    def get_nodes(self):
        dbdata_nodes = self.dbdata_nodes
        nodes = {}
        for name, dbdata in dbdata_nodes.items():
            node = DBNode(uuid=dbdata["uuid"])  # , self.daemon_name)
            nodes[node.name] = node
        return nodes

    @skip_ref_node
    def pause_node(self, name):
        """Pause node.

        Args:
            name (str): name of the node to be paused
        """

        send_message_to_queue(
            broker_queue_name, f"{self.uuid},node,{name}:action:PAUSE"
        )

    @skip_ref_node
    def play_node(self, name):
        """Play node.

        Args:
            name (str): name of the node to be played
        """

        send_message_to_queue(broker_queue_name, f"{self.uuid},node,{name}:action:PLAY")

    @skip_ref_node
    def skip_node(self, name):
        """Skip node.

        Args:
            name (str): name of the node to be skipd
        """

        send_message_to_queue(broker_queue_name, f"{self.uuid},node,{name}:action:SKIP")

    @skip_ref_node
    def reset_node(self, name, launch=False):
        """Reset node and all its child nodes.

        Args:
            name (str): name of the node to be paused
        """

        if launch:
            send_message_to_queue(
                broker_queue_name, f"{self.uuid},node,{name}:action:RESET_LAUNCH"
            )
        else:
            send_message_to_queue(
                broker_queue_name, f"{self.uuid},node,{name}:action:RESET"
            )

    @skip_ref_node
    def cancel_node(self, name):
        """Cancel node."""
        from scinode.database.client import db_node

        uuid = self.record["nodes"][name]["uuid"]
        logger.debug("cancel node, name={}, uuid={}".format(name, uuid))
        newvalues = {"$set": {"action": "CANCEL"}}
        db_node.update_one({"uuid": uuid}, newvalues)

    def reset(self):
        """Reset nodetree and all its nodes.

        Args:
            name (str): name of the node to be paused
        """

        logger.debug("Reset nodetree: {}".format(self.name))
        send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,action:RESET")

    def write_log(self, log, daemon=False, database=True):
        if daemon:
            print(log)
        if database:
            old_log = self.db.find_one({"uuid": self.uuid}, {"_id": 0, "log": 1})["log"]
            log = old_log + log
            self.update_db_keys({"log": log})
