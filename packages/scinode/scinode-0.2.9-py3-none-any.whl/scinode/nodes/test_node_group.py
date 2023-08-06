from scinode.core.node import Node


class TestSqrtAdd(Node):

    identifier: str = "TestSqrtAdd"
    name = "TestSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_node_group(self):
        from scinode.nodetree import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            daemon_name=self.daemon_name,
        )
        sqrt1 = nt.nodes.new("TestSqrt", "sqrt1")
        sqrt2 = nt.nodes.new("TestSqrt", "sqrt2")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt1.outputs[0], add1.inputs[0])
        nt.links.new(sqrt2.outputs[0], add1.inputs[1])
        nt.group_properties = [
            ("sqrt1", "t", "t1"),
            ("add1", "t", "t2"),
        ]
        nt.group_inputs = [
            ("sqrt1", "x", "x"),
            ("sqrt2", "x", "y"),
        ]
        nt.group_outputs = [("add1", "Result", "Result")]
        return nt


class TestNestedSqrtAdd(Node):

    identifier: str = "TestNestedSqrtAdd"
    name = "TestNestedSqrtAdd"
    catalog = "Test"
    node_type: str = "GROUP"

    def get_node_group(self):
        from scinode.nodetree import NodeTree

        nt = NodeTree(
            name=self.name,
            uuid=self.uuid,
            parent_node=self.uuid,
            daemon_name=self.daemon_name,
        )
        sqrt_add1 = nt.nodes.new("TestSqrtAdd", "sqrt_add1")
        sqrt_add2 = nt.nodes.new("TestSqrtAdd", "sqrt_add2")
        add1 = nt.nodes.new("TestAdd", "add1")
        nt.links.new(sqrt_add1.outputs[0], add1.inputs[0])
        nt.links.new(sqrt_add2.outputs[0], add1.inputs[1])
        nt.group_inputs = [("sqrt_add1", "x", "x"), ("sqrt_add2", "x", "y")]
        nt.group_outputs = [["add1", "Result", "Result"]]
        return nt


node_list = [
    TestSqrtAdd,
    TestNestedSqrtAdd,
]
