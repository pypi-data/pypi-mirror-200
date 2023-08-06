from uuid import uuid1
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NodeSocket:
    """Socket object.
    Input and ouput sockets of a Node.

    Attributes:
        name (str): socket name.
        node (Node): node this socket belongs to.
        type (str): socket type.
        index (int): index of this socket in the SocketCollection.
        links (list): links
        property (unknown):
        link_limit (int): maxminum number of link.
    """

    identifier: str = "NodeSocket"
    default_value: float = 0.0
    link_limit: int = 1

    def __init__(self, name, node=None, type="INPUT", index=0, uuid=None) -> None:
        """Init a instance of NodeSocket.

        Args:
            name (str): name of the socket
            node (_type_, optional): _description_. Defaults to None.
            index (int, optional): _description_. Defaults to 0.
        """
        self.name = name
        self.node = node
        self.type = type
        self.index = index
        self.uuid = uuid or str(uuid1())
        self.links = []
        self.property = None

    def to_dict(self):
        """Export to a dictionary.
        Data to be saved to database. For basic JSON support.
        """
        # data from socket itself
        dbdata = {
            "name": self.name,
            "identifier": self.identifier,
            "uuid": self.uuid,
            "node_uuid": self.node.uuid,
            "type": self.type,
            "link_limit": self.link_limit,
            "links": [],
            "serialize": self.get_serialize(),
            "deserialize": self.get_deserialize(),
        }
        # data from linked sockets
        for link in self.links:
            if self.type == "INPUT":
                dbdata["links"].append(
                    {
                        "from_node": link.from_node.name,
                        "from_socket": link.from_socket.name,
                        "from_socket_uuid": link.from_socket.uuid,
                    }
                )
            else:
                dbdata["links"].append(
                    {
                        "to_node": link.to_node.name,
                        "to_socket": link.to_socket.name,
                        "to_socket_uuid": link.to_socket.uuid,
                    }
                )
        return dbdata

    def add_link(self, link):
        """Handle multi-link here"""
        pass

    def add_property(self, identifier, name=None, data={}):
        """Add property to this socket."""
        from scinode.properties import property_pool
        import difflib

        if identifier not in property_pool:
            properties = difflib.get_close_matches(identifier, property_pool)
            if len(properties) == 0:
                msg = "Property: {} is not defined.".format(identifier)
            else:
                msg = "Property: {} is not defined. Do you mean {}".format(
                    identifier, ", ".join(properties)
                )
            raise Exception(msg)
        ItemClass = property_pool[identifier]
        property = ItemClass(name, **data)
        self.property = property

    @classmethod
    def from_dict(cls, data):
        """Rebuild Socket object from dictionary representation."""
        socket = cls(data["name"], type=data["type"])
        return socket

    @property
    def value(self):
        return self.node.properties[self.name].value

    @value.setter
    def value(self, value):
        self.node.properties[self.name].value = value

    def __repr__(self) -> str:
        s = ""
        s += '{}(name="{}", node="{}", value = {})'.format(
            self.__class__.__name__, self.name, self.node.name, self.property.value
        )
        return s
