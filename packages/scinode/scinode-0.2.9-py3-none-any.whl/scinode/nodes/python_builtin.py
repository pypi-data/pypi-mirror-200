from scinode.core.node import Node


class IntNode(Node):
    """Output a int value."""

    identifier = "Int"
    name = "Int"
    catalog = "Input"

    args = ["Int"]

    def create_properties(self):
        self.properties.new("Int", "Int", data={"default": 0})

    def create_sockets(self):
        self.outputs.new("Int", "Int")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "int",
            "type": "function",
        }


class FloatNode(Node):
    """Output a float value."""

    identifier = "Float"
    name = "Float"
    catalog = "Input"

    args = ["Float"]

    def create_properties(self):
        self.properties.new("Float", "Float", data={"default": 0.0})

    def create_sockets(self):
        self.outputs.new("Float", "Float")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "float",
            "type": "function",
        }


class BoolNode(Node):
    """Output a bool value."""

    identifier = "Bool"
    name = "Bool"
    catalog = "Input"

    args = ["Bool"]

    def create_properties(self):
        self.properties.new("Bool", "Bool", data={"default": True})

    def create_sockets(self):
        self.outputs.new("Bool", "Bool")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "bool",
            "type": "function",
        }


class StrNode(Node):
    """Output a string."""

    identifier = "String"
    name = "String"
    catalog = "Input"

    args = ["String"]

    def create_properties(self):
        self.properties.new("String", "String", data={"default": ""})

    def create_sockets(self):
        self.outputs.new("String", "String")

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "str",
            "type": "function",
        }


class Getattr(Node):
    """The Getattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: getattr()

    Results:
        A pyhont object.

    Example:

    >>> att = nt.nodes.new("Getattr")
    >>> att.properties["Name"].value = "real"

    """

    identifier: str = "Getattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("String", "Name")
        inp.property.value = "__class__"
        self.outputs.new("General", "Result")
        self.args = ["Source", "Name"]

    def get_executor(self):
        return {
            "path": "builtins",
            "name": "getattr",
            "type": "function",
        }


class Setattr(Node):
    """The Setattr node sets the value of the attribute of an object.

    Executor:
        Python builtin function: setattr()

    Results:
        A pyhont object.

    Example:

    >>> nt = NodeTree(name="test_setattr")
    >>> person1 = nt.nodes.new("TestPerson", "person1")
    >>> str1 = nt.nodes.new("TestString", "str1")
    >>> str1.properties["String"].value = "Peter"
    >>> att = nt.nodes.new("Setattr")
    >>> att.properties["Name"].value = "name"
    >>> nt.links.new(person1.outputs[0], att.inputs["Source"])
    >>> nt.links.new(str1.outputs[0], att.inputs["Value"])

    """

    identifier: str = "Setattr"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Name")
        inp.property.value = "__class__"
        self.inputs.new("General", "Value")
        self.outputs.new("General", "Result")
        self.args = ["Source", "Name", "Value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setattr",
            "type": "function",
        }


class Getitem(Node):
    """The Getitem node suppors index lookups.

    Executor:
        Python builtin function: __getitem__()

    Results:
        A pyhont object.

    Example:

    >>> getitem1 = nt.nodes.new("Getitem", "getitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> nt.links.new(nt.nodes["power1"].outputs[0], getitem1.inputs["Source"])
    >>> nt.links.new(arange1.outputs[0], getitem1.inputs["Index"])
    """

    identifier: str = "Getitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Index")
        inp.property.value = 0
        self.outputs.new("General", "Result")
        self.args = ["Source", "Index"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "getitem",
            "type": "function",
        }


class Setitem(Node):
    """The Setitem node is used for assigning a value to an item.

    Executor:
        Python builtin function: __setitem__()

    Results:
        A pyhont object.

    Example:

    >>> setitem1 = nt.nodes.new("Setitem", "setitem1")
    >>> arange1 = nt.nodes.new("ScinodeNumpy", "arange")
    >>> arange1.set({"function": "arange", "start": 1, "stop": 5, "step": 2})
    >>> linspace2 = nt.nodes.new("ScinodeNumpy", "linspace2")
    >>> linspace2.set({"function": "linspace", "start": 11, "stop": 15, "num": 2})
    >>> nt.links.new(nt.nodes["linspace1"].outputs[0], setitem1.inputs["Source"])
    >>> nt.links.new(arange1.outputs[0], setitem1.inputs["Index"])
    >>> nt.links.new(linspace2.outputs[0], setitem1.inputs["Value"])
    """

    identifier: str = "Setitem"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        inp = self.inputs.new("General", "Index")
        inp.property.value = 0
        self.inputs.new("General", "Value")
        self.outputs.new("General", "Result")
        self.args = ["Source", "Index", "Value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "setitem",
            "type": "function",
        }


class Index(Node):
    """To find index of the first occurrence of an element
    in a given Python List or numpy array.

    Executor:
        Python builtin function: list.index(), numpy.where()

    Results:
        Index.

    Example:

    """

    identifier: str = "Index"
    node_type: str = "Normal"
    catalog = "Builtin"

    def create_properties(self):
        pass

    def create_sockets(self):
        self.inputs.clear()
        self.outputs.clear()
        self.inputs.new("General", "Source")
        self.inputs.new("General", "Value")
        self.outputs.new("General", "Index")
        self.args = ["Source", "Value"]

    def get_executor(self):
        return {
            "path": "scinode.executors.python",
            "name": "index",
            "type": "function",
        }


node_list = [
    IntNode,
    FloatNode,
    BoolNode,
    StrNode,
    Getattr,
    Setattr,
    Getitem,
    Setitem,
    Index,
]
