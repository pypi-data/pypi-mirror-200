"""NodeTree
A nodetree is a workflow.
"""

import logging
from scinode.core.collection import NodeCollection, LinkCollection, NodeTreeCollection
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.config import broker_queue_name
from uuid import uuid1

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def skip_ref_node(func):
    def wrapper(self, name, **kwargs):
        if self.nodes[name].node_type == "REF":
            raise Exception("Can not change state of a reference node")
        return func(self, name, **kwargs)

    return wrapper


class NodeTree:
    """Nodetree is a collection of nodes and links.

    Attributes:

    daemon_name: str
        name of the daemon which will run this nodetree.
        Default value: localhost
    uuid: str
        uuid of this nodetree.
    state: str
        state of this nodetree.
    action: str
        action of this nodetree.
    platform: str
        platform that used to creat this nodetree.

    Examples:

    >>> from scinode.nodetree import NodeTree
    >>> nt = NodeTree(name="my_first_nodetree")

    add nodes:

    >>> float1 = nt.nodes.new("TestFloat", name = "float1")
    >>> add1 = nt.nodes.new("TestAdd", name = "add1")

    add links:

    >>> nt.links.new(float1.outputs[0], add1.inputs[0])

    Launch the nodetree:

    >>> nt.launch()

    """

    daemon_name: str = "localhost"
    platform: str = "scinode"
    uuid: str = ""
    group_properties = []
    group_inputs = []
    group_outputs = []

    def __init__(
        self,
        name="NodeTree",
        uuid=None,
        daemon_name="localhost",
        parent="",
        parent_node="",
        scatter_node="",
        scattered_label="",
    ) -> None:
        """_summary_

        Args:
            name (str, optional): name of the nodetree.
                Defaults to "NodeTree".
            uuid (str, optional): uuid of the nodetree.
                Defaults to None.
            daemon_name (str, optional): name of the daemon.
                Defaults to "localhost".
            parent (str, optional): uuid of the parent nodetree.
                Defaults to ''.
        """
        self.name = name
        self.uuid = uuid or str(uuid1())
        self.daemon_name = daemon_name
        self.parent = parent
        self.parent_node = parent_node
        self.scatter_node = scatter_node
        self.scattered_label = scattered_label
        self.nodetrees = NodeTreeCollection(self)
        self.nodes = NodeCollection(self)
        self.links = LinkCollection(self)
        self.state = "CREATED"
        self.action = "NONE"
        self.description = ""
        self.log = ""
        logger.info("Create NodeTree: {}".format(self.name))

    def launch(self, daemon_name=None):
        """Launch the nodetree."""
        from scinode.engine.send_to_queue import launch_nodetree

        logger.info("Launch NodeTree: {}".format(self.name))
        if daemon_name is not None:
            self.daemon_name = daemon_name
        self.save()
        launch_nodetree(self.daemon_name, self.uuid)

    def save(self):
        """Save nodetree to database."""
        from scinode.engine.nodetree_launch import LaunchNodeTree

        logger.debug("Save nodetree to database: {}".format(self.name))
        self.state = "CREATED"
        ntdata = self.to_dict()
        lnt = LaunchNodeTree(ntdata)
        lnt.save()

    def to_dict(self, short=False):
        """To dict

        Returns:
            dict: nodetree data
        """
        from scinode.version import __version__

        metadata = self.get_metadata()
        nodes = self.nodes_to_dict(short=short)
        links = self.links_to_dict()
        data = {
            "version": "scinode@{}".format(__version__),
            "uuid": self.uuid,
            "name": self.name,
            "state": self.state,
            "action": self.action,
            "error": "",
            "metadata": metadata,
            "nodes": nodes,
            "links": links,
            "description": self.description,
            "log": self.log,
        }
        return data

    def get_metadata(self):
        """metadata to dict"""
        metadata = {
            "daemon_name": self.daemon_name,
            "parent": self.parent,
            "platform": self.platform,
            "parent_node": self.parent_node,
            "scatter_node": self.scatter_node,
            "scattered_label": self.scattered_label,
        }
        return metadata

    def nodes_to_dict(self, short=False):
        """nodes to dict"""
        # save all relations using links
        nodes = {}
        for node in self.nodes:
            if short:
                nodes[node.name] = node.to_dict(short=short)
            else:
                nodes[node.name] = node.to_dict(daemon_name=self.daemon_name)
        return nodes

    def links_to_dict(self):
        """links to dict"""
        # save all relations using links
        links = []
        for link in self.links:
            links.append(link.to_dict())
        # logger.debug("Done")
        return links

    def to_yaml(self):
        """Export to a yaml format data.
        Results of the nodes are not exported."""
        import yaml

        data = self.to_dict()
        for name, node in data["nodes"].items():
            node.pop("results", None)
        s = yaml.dump(data, sort_keys=False)
        return s

    def reset(self):
        """Reset all node."""
        from scinode.orm.db_nodetree import DBNodeTree

        ent = DBNodeTree(uuid=self.uuid)
        ent.reset()
        self.update()

    def update(self):
        from scinode.database.client import scinodedb

        query = {"uuid": self.uuid}
        data = scinodedb["nodetree"].find_one(
            query, {"index": 1, "state": 1, "action": 1, "nodes": 1}
        )
        self.index = data["index"]
        self.state = data["state"]
        self.action = data["action"]
        self.update_nodes(data["nodes"])

    def update_nodes(self, data):
        for node in self.nodes:
            node.state = data[node.name]["state"]
            node.action = data[node.name]["action"]
            node.update()

    @skip_ref_node
    def reset_node(self, name):
        """Reset node.

        Args:
            name (str): name of the node to be reseted
        """

        msg = f"{self.uuid},node,{name}:action:RESET"
        send_message_to_queue(broker_queue_name, msg)

    @skip_ref_node
    def pause_node(self, name):
        """pause node.

        Args:
            name (str): name of the node to be paused
        """

        msg = f"{self.uuid},node,{name}:state:PAUSED"
        send_message_to_queue(broker_queue_name, msg)

    @skip_ref_node
    def play_node(self, name):
        """play node.

        Args:
            name (str): name of the node to be played
        """

        msg = f"{self.uuid},node,{name}:state:CREATED"
        send_message_to_queue(broker_queue_name, msg)

    @classmethod
    def from_dict(cls, ntdata):
        """Rebuild nodetree from dict ntdata.

        Args:
            ntdata (dict): data of the nodetree.

        Returns:
            Nodedtree: a nodetree
        """
        # subnodetree
        nt = cls(
            name=ntdata["name"],
            uuid=ntdata.get("uuid"),
            daemon_name=ntdata["metadata"]["daemon_name"],
        )
        # print("from_dict: ", nt.uuid)
        for key in ["state", "action", "description"]:
            if ntdata.get(key):
                setattr(nt, key, ntdata.get(key))
        # TODO we need read all the metadata
        nt.parent = ntdata["metadata"].get("parent", "")
        nt.parent_node = ntdata["metadata"].get("parent_node", "")
        for name, ndata in ntdata["nodes"].items():
            # print("Node name: {}, type: {}".format(name, ndata["metadata"]["node_type"]))
            node = nt.nodes.new(
                ndata["metadata"]["identifier"],
                name=name,
                uuid=ndata.pop("uuid", None),
            )
            node.update_from_dict(ndata)
        # re-build links
        for link in ntdata["links"]:
            nt.links.new(
                nt.nodes[link["from_node"]].outputs[link["from_socket"]],
                nt.nodes[link["to_node"]].inputs[link["to_socket"]],
            )
        return nt

    @classmethod
    def from_yaml(cls, filename=None, string=None):
        """Build nodetree from yaml file.

        Args:
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            Nodetree: _description_
        """
        import yaml
        from scinode.utils.nodetree import yaml_to_dict
        from pprint import pprint

        # load data
        if filename:
            with open(filename, "r") as f:
                ntdata = yaml.safe_load(f)
        elif string:
            ntdata = yaml.safe_load(string)
        else:
            raise Exception("Please specific a filename or yaml string.")
        ntdata = yaml_to_dict(ntdata)
        nt = cls.from_dict(ntdata)
        return nt

    def copy(self):
        """Copy nodetree.
        Reset uuid of nodetree and nodes.
        """
        ntdata = self.to_dict()
        # reset uuid for nodetree
        ntdata["uuid"] = str(uuid1())
        # reset uuid for nodes
        for name, node in ntdata["nodes"].items():
            node["uuid"] = str(uuid1())
        nodetree = self.from_dict(ntdata)
        # print("copy nodetree: ", nodetree)
        return nodetree

    @classmethod
    def load_from_db(cls, uuid):
        """Load data from database.
        1) attributes
        2) nodes
        3) links
        """
        from scinode.utils.node import deserialize
        from scinode.database.client import scinodedb

        ntdata = scinodedb["nodetree"].find_one({"uuid": uuid})
        # populate the nodes data
        nodes = ntdata.pop("nodes")
        ntdata["nodes"] = {}
        for name, node in nodes.items():
            ndata = scinodedb["node"].find_one({"uuid": node["uuid"]})
            ndata["properties"] = deserialize(ndata["properties"])
            ntdata["nodes"][name] = ndata
        nodetree = cls.from_dict(ntdata)
        return nodetree

    def copy_nodes_to_new_nodetree(self, from_nodes, prefix):
        from scinode.nodetree import NodeTree

        print("    Add new NodeTree")
        nt = NodeTree(
            name="{}_{}".format(self.name, prefix),
            parent=self.uuid,
            daemon_name=self.daemon_name,
        )
        # save nodetree to database
        nt.init_db()
        nt.load_from_db(uuid=self.uuid, nodes=from_nodes)
        return nt

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)
        else:
            return None

    def __repr__(self) -> str:
        s = ""
        s += 'NodeTree(name="{}, uuid="{}")\n'.format(self.name, self.uuid)
        return s


if __name__ == "__main__":
    nt = NodeTree("test")
    nt.nodes.new("TestFloat")
    nt1 = nt.copy()
    assert nt1.uuid != nt.uuid
