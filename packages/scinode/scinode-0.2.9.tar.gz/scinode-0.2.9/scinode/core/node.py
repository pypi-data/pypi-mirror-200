"""Node
"""
from scinode.core.collection import (
    PropertyCollection,
    InputSocketCollection,
    OutputSocketCollection,
)
from uuid import uuid1

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Node:
    """Base class for Node.

    Attributes:

    identifier: str
        The identifier is used for loading the Node.
    node_type: str
        type of this node. "Normal", "REF", "GROUP".
    id: int
        node id in the nodetree.
    nodetree_uuid: str
        uuid of the nodetree this node belongs to.
    daemon_name: str
        name of the daemon which will run this node.
    counter: int
        number of time this node has been executed.
    args: list
        postional arguments of the exector.
    kwargs: list
        keyword arguments of the exector.
    platform: str
        platform that used to creat this node.
    scattered_from: str
        scattered_from node which is copied.

    Examples:

    add nodes:

    >>> float1 = nt.nodes.new("TestFloat", name = "float1")
    >>> add1 = nt.nodes.new("TestDelayAdd", name = "add1")
    """

    identifier: str = "Node"
    node_type: str = "Normal"
    id: int = 0
    nodetree_uuid: str = ""
    daemon_name: str = ""
    counter: int = 0
    platform: str = "scinode"
    catalog: str = "Node"
    args = []
    kwargs = []
    group_inputs = []
    group_outputs = []

    def __init__(
        self,
        id=1,
        name=None,
        uuid=None,
        nodetree=None,
        scattered_from="",
        scattered_label="",
        scatter_node="",
    ) -> None:
        self.id = id
        self.name = name or "{}{}".format(self.identifier, id)
        self.uuid = uuid or str(uuid1())
        self.nodetree = nodetree
        self.scattered_from = scattered_from
        self.scattered_label = scattered_label
        self.scatter_node = scatter_node
        self.ref_uuid = ""
        self.copy_uuid = ""
        self.properties = PropertyCollection(self)
        self.inputs = InputSocketCollection(self)
        self.outputs = OutputSocketCollection(self)
        self.executor = None
        self.state = "CREATED"
        self.action = "NONE"
        self.position = [30 * self.id, 30 * self.id]
        self.description = ""
        self.log = ""
        self.ntg = self.get_node_group() if self.node_type.upper() == "GROUP" else None
        self.create_properties()
        self.create_sockets()
        logger.info("Create {}: {}".format(self.node_type, self.name))

    def create_properties(self):
        """Create properties for this node.
        If this node is a group node, create properties based on the exposed properties.
        """
        self.properties.clear()
        if self.node_type.upper() == "GROUP":
            self.create_group_properties()

    def create_group_properties(self):
        """Create properties based on the exposed properties."""
        for prop in self.group_properties:
            node, prop_name, new_prop_name = prop
            if prop_name not in self.ntg.nodes[node].properties.keys():
                raise ValueError(
                    "Property {} does not exist in the properties of node {}".format(
                        prop_name, node
                    )
                )
            p = self.ntg.nodes[node].properties[prop_name].copy()
            p.name = new_prop_name
            # TODO add the default value to group property
            self.properties.append(p)

    def create_sockets(self):
        """Create input and output sockets for this node.
        If this node is a group node, create sockets based on group inputs and outputs.
        """
        self.inputs.clear()
        self.outputs.clear()
        if self.node_type.upper() == "GROUP":
            self.create_group_sockets()

    def create_group_sockets(self):
        """Create input and output sockets based on group inputs
        and outputs.

        group_inputs = [
            ["add1", "x", "x"],
            ["add1", "y", "y"],
        ]
        """
        for input in self.group_inputs:
            node, socket, name = input
            if socket not in self.ntg.nodes[node].inputs.keys():
                raise ValueError(
                    "Socket {} does not exist in the intputs of node {}".format(
                        socket, node
                    )
                )
            identifier = self.ntg.nodes[node].inputs[socket].identifier
            self.inputs.new(identifier, name)
        for output in self.group_outputs:
            node, socket, name = output
            if socket not in self.ntg.nodes[node].outputs.keys():
                raise ValueError(
                    "Socket {} does not exist in the outputs of node {}".format(
                        socket, node
                    )
                )
            identifier = self.ntg.nodes[node].outputs[socket].identifier
            self.outputs.new(identifier, name)

    def reset(self):
        """Reset this node and all its child nodes to "CREATED".

        Note, even through the core principle require that each node
        run independently. This action will set the state of this node and
        all its child nodes to "CREATED". Because this is execute by human.
        In order to do that, we need use the nodetree to reset its child nodes.
        """
        from scinode.orm.db_nodetree import DBNodeTree

        if self.node_type not in ["REF"]:
            ent = DBNodeTree(uuid=self.uuid)
            ent.reset_node(self.name)
        self.update()

    def pre_save(self):
        """Pre action before save data to database.
        If this node is a group node, save the nodetree group.
        """
        if self.node_type.upper() == "GROUP":
            self.ntg.daemon_name = self.daemon_name
            self.ntg.save()

    def pre_load(self):
        """Pre action before load data from database."""
        pass

    @property
    def group_properties(self):
        return self.ntg.group_properties if self.ntg else []

    @property
    def group_inputs(self):
        return self.ntg.group_inputs if self.ntg else []

    @property
    def group_outputs(self):
        return self.ntg.group_outputs if self.ntg else []

    @property
    def node_group(self):
        return self.get_node_group()

    def get_node_group(self):
        from scinode.nodetree import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            daemon_name=self.daemon_name,
        )
        return nt

    def to_dict(self, short=False, daemon_name="localhost"):
        """Save all datas, include properties, input and output sockets.

        This will be called when execute nodetree
        """
        from scinode.version import __version__
        import json
        import hashlib

        logger.debug("save_to_db: {}".format(self.name))

        if not self.daemon_name:
            self.daemon_name = daemon_name
        self.pre_save()

        if short:
            data = {
                "name": self.name,
                "identifier": self.identifier,
                "node_type": self.node_type,
                "uuid": self.uuid,
            }
        else:
            metadata = self.get_metadata()
            properties = self.properties_to_dict()
            input_sockets = self.input_sockets_to_dict()
            output_sockets = self.output_sockets_to_dict()
            executor = self.executor_to_dict()
            data = {
                "version": "scinode@{}".format(__version__),
                "uuid": self.uuid,
                "name": self.name,
                "id": self.id,
                "state": self.state,
                "action": self.action,
                "error": "",
                "metadata": metadata,
                "properties": properties,
                "inputs": input_sockets,
                "outputs": output_sockets,
                "executor": executor,
                "position": self.position,
                "description": self.description,
                "log": self.log,
                "hash": "",
            }
            # calculate the hash of metadata
            hash_metadata = {
                "executor": executor,
                "args": self.args,
                "kwargs": self.kwargs,
            }
            data["metadata"]["hash"] = hashlib.md5(
                json.dumps(hash_metadata).encode("utf-8")
            ).hexdigest()
        return data

    def get_metadata(self):
        """Export metadata to a dictionary."""
        metadata = {
            "node_type": self.node_type,
            "catalog": self.catalog,
            "identifier": self.identifier,
            "nodetree_uuid": self.nodetree.uuid,
            "ref_uuid": self.ref_uuid,
            "copy_uuid": self.copy_uuid,
            "platform": self.platform,
            "scattered_from": self.scattered_from,
            "scattered_label": self.scattered_label,
            "scatter_node": self.scatter_node,
            "counter": self.counter,
            "args": self.args,
            "kwargs": self.kwargs,
            "group_properties": self.group_properties,
            "group_inputs": self.group_inputs,
            "group_outputs": self.group_outputs,
            "daemon_name": self.daemon_name,
        }
        if not self.daemon_name:
            metadata.update({"daemon_name": self.nodetree.daemon_name})
        else:
            metadata.update({"daemon_name": self.daemon_name})
        return metadata

    def properties_to_dict(self):
        """Export properties to a dictionary.
        This data will be used for calculation.
        """
        properties = {}
        for p in self.properties:
            properties[p.name] = p.to_dict()
        # properties from inputs
        # data from property
        for input in self.inputs:
            if input.property is not None:
                properties[input.name] = input.property.to_dict()
            else:
                properties[input.name] = None
        return properties

    def input_sockets_to_dict(self):
        """Export input sockets to a dictionary."""
        # save all relations using links
        inputs = []
        for socket in self.inputs:
            inputs.append(socket.to_dict())
        return inputs

    def output_sockets_to_dict(self):
        """Export output sockets to a dictionary."""
        # save all relations using links
        outputs = []
        for socket in self.outputs:
            outputs.append(socket.to_dict())
        return outputs

    def executor_to_dict(self):
        """Export executor dictionary to a dictionary.
        Three kinds of executor:
        - Python built-in function. e.g. getattr
        - User defined function
        - User defined class.
        """
        executor = self.get_executor() or self.executor
        if executor is None:
            return executor
        if "name" not in executor:
            executor["name"] = executor["path"].split(".")[-1]
            executor["path"] = executor["path"][0 : -(len(executor["name"]) + 1)]
        if "type" not in executor:
            executor["type"] = "function"
        return executor

    @classmethod
    def from_dict(cls, data):
        """Rebuild Node from dict data."""
        # print("data: ", data)
        node = cls(name=data["name"], uuid=data["uuid"])
        # load properties
        node.update_from_dict(data)
        return node

    def update_from_dict(self, data):
        """udpate node from dict data.
        Set metadata and properties.
        """
        for key in ["uuid", "state", "action", "description", "hash", "position"]:
            if data.get(key):
                setattr(self, key, data.get(key))
        self.daemon_name = data["metadata"].get("daemon_name", "")
        # properties first, because the socket may be dynamic
        for name in self.properties.keys():
            if name in data["properties"]:
                self.properties[name].value = data["properties"][name]["value"]
        # inputs
        # print("inputs: ", data.get("inputs", None))
        if data.get("inputs", None):
            for i in range(len(data["inputs"])):
                if data["inputs"][i].get("uuid", None):
                    self.inputs[i].uuid = data["inputs"][i]["uuid"]
                if self.inputs[i].name in data["properties"]:
                    p = data["properties"][self.inputs[i].name]
                    self.inputs[i].property.value = p["value"]
        # outputs
        if data.get("outputs", None):
            for i in range(len(data["outputs"])):
                if data["outputs"][i].get("uuid", None):
                    self.outputs[i].uuid = data["outputs"][i]["uuid"]

    @classmethod
    def update_from_yaml(cls, filename=None, string=None):
        """update db node from yaml file.

        Args:
            filename (str, optional): _description_. Defaults to None.
            string (str, optional): _description_. Defaults to None.

        Returns:
            node: _description_
        """
        import yaml
        from scinode.utils.node import yaml_to_dict
        from pprint import pprint

        # load data
        if filename:
            with open(filename, "r") as f:
                ndata = yaml.safe_load(f)
        elif string:
            ndata = yaml.safe_load(string)
        else:
            raise Exception("Please specific a filename or yaml string.")
        ndata = yaml_to_dict(ndata)
        nt = cls.load_from_db(ndata["uuid"])
        return nt

    @classmethod
    def load_from_db(cls, uuid):
        """Load Node data from database."""
        from scinode.utils.node import get_node_data

        print("    Load data for node: uuid={}".format(uuid))
        ndata = get_node_data({"uuid": uuid})
        cls.pre_load(ndata)
        node = cls.from_dict(ndata)
        return node

    def copy(self, name):
        node = self.__class__(name=name, uuid=None, nodetree_uuid=self.nodetree_uuid)
        node.inputs.copy()
        node.outputs.copy()
        return node

    def get_executor(self):
        """Get the default executor."""
        executor = None
        if self.node_type.upper() == "GROUP":
            executor = {
                "path": "scinode.executors.built_in",
                "name": "NodeGroup",
                "type": "class",
            }
        return executor

    def get_results(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.utils.node import get_results

        results = get_results(self.uuid)
        return results

    def update(self):
        """Update node."""
        from scinode.database.client import scinodedb

        query = {"uuid": self.uuid}
        data = scinodedb["node"].find_one(
            query, {"state": 1, "action": 1, "results": 1, "metadata.counter": 1}
        )
        self.counter = data["metadata"]["counter"]
        self.results = self.get_results()

    def ref_to(self, uuid):
        """Set reference node."""
        from scinode.database.client import scinodedb

        self.node_type = "REF"
        self.ref_uuid = uuid
        ndata = scinodedb["node"].find_one(
            {"uuid": uuid}, {"_id": 0, "metadata.identifier": 1, "outputs": 1}
        )
        assert ndata != None
        assert self.identifier == ndata["metadata"]["identifier"]
        for i in range(len(ndata["outputs"])):
            self.outputs[i].uuid = ndata["outputs"][i]["uuid"]

    def __repr__(self) -> str:
        s = ""
        s += 'Node(name="{}", uuid="{}", inputs = ['.format(self.name, self.uuid)
        for input in self.inputs:
            s += '"{}", '.format(input.name)
        s += "], outputs = ["
        for output in self.outputs:
            s += '"{}", '.format(output.name)
        s += "])\n"
        return s

    def set(self, data):
        """Set properties by a dict.

        Args:
            data (dict): _description_
        """
        from scinode.core.socket import NodeSocket

        for key, value in data.items():
            if key in self.properties.keys():
                self.properties[key].value = value
            elif key in self.inputs.keys():
                if isinstance(value, NodeSocket):
                    self.nodetree.links.new(value, self.inputs[key])
                else:
                    self.inputs[key].property.value = value
            else:
                raise Exception("No property named {}".format(key))

    def get(self, key):
        """Get the value of property by key.

        Args:
            key (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.properties[key].value


def build_node_from_json(dbdata):
    import importlib

    module = importlib.import_module("{}".format(dbdata["node_path"]))
    node_type = getattr(module, dbdata["node_type"])
    node = node_type.from_json(dbdata)
    return node
