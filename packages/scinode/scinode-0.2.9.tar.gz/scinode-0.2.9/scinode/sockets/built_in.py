from scinode.core.socket import NodeSocket
from scinode.serialization.built_in import SerializeJson, SerializePickle


class SocketGeneral(NodeSocket, SerializePickle):
    """General socket."""

    identifier: str = "General"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("General", name, data={"default": None})


class SocketFloat(NodeSocket, SerializeJson):
    """Float socket."""

    identifier: str = "Float"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("Float", name, data={"default": 0.0})


class SocketInt(NodeSocket, SerializeJson):
    """Int socket."""

    identifier: str = "Int"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("Int", name, data={"default": 0})


class SocketString(NodeSocket, SerializeJson):
    """String socket."""

    identifier: str = "String"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("String", name, data={"default": ""})


class SocketBool(NodeSocket, SerializeJson):
    """Bool socket."""

    identifier: str = "Bool"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("Bool", name, data={"default": False})


class SocketBaseList(NodeSocket, SerializeJson):
    """Socket with a BaseList property."""

    identifier: str = "BaseList"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("BaseList", name, data={"default": {}})


class SocketBaseDict(NodeSocket, SerializeJson):
    """Socket with a BaseDict property."""

    identifier: str = "BaseDict"

    def __init__(self, name, node=None, type="INPUT", index=0) -> None:
        super().__init__(name, node, type, index)
        self.add_property("BaseDict", name, data={"default": {}})


socket_list = [
    SocketGeneral,
    SocketInt,
    SocketFloat,
    SocketString,
    SocketBool,
    SocketBaseDict,
    SocketBaseList,
]
