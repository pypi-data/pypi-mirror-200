from scinode.core.executor import Executor


class ScinodeSwitch(Executor):
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
        from scinode.utils.db import replace_one
        from scinode.utils.node import serialize_item
        from scinode.database.client import scinodedb

        print("    Run for Switch node")
        dbdata = self.dbdata
        # nodetree data
        nt = DBNodeTree(uuid=dbdata["metadata"]["nodetree_uuid"])
        # because we skip the daemon to set the state
        # we have to update the result manully here
        data = self.dbdata["outputs"][0]
        data["value"] = self.kwargs["Input"]
        # print(data)
        replace_one(serialize_item(data), scinodedb["data"])
        # set node state to be finished to avoid deadblock
        # find all children nodes of the "switch" node
        if self.kwargs["Switch"]:
            # reset all nodes and launch
            print("reset node")
            nt.reset_node(dbdata["name"], launch=True)
        else:
            # skip all nodes
            print("skip node")
            nt.skip_node(dbdata["name"])
        this_results = (self.kwargs["Input"],)
        return this_results
