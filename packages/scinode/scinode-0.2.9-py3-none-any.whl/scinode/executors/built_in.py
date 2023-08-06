from scinode.core.executor import Executor


class PropertyToSocket(Executor):
    """Out the properties as sockets."""

    def run(self):
        results = ()
        outputs = self.dbdata["outputs"]
        # all kwargs as one socket
        if len(outputs) == 1 and len(self.kwargs) != 1:
            return (self.kwargs,)
        # one kwarg as one socket
        # here we need to check
        for socket in outputs:
            results += (self.kwargs[socket["name"]],)
        return results


class ResultToSocket(Executor):
    """Out the result as sockets."""

    def run(self):
        from scinode.utils.node import get_results

        db_results = get_results(self.uuid)
        results = ()
        for result in db_results:
            results += (result["value"],)
        return results


def InputToSocket(*args):
    """Out the input as sockets."""
    results = ()
    for x in args:
        results += (x,)
    return results


class NodeGroup(Executor):
    """Out the properties as sockets."""

    def run(self):
        """For node group.
        Run the nodetree.
        Connections to the Group Input will become attached
        to the input sockets of the coresponding nodes.
        """
        from scinode.orm.db_nodetree import DBNodeTree
        from scinode.utils.node import get_node_data, serialize

        nt = DBNodeTree(uuid=self.uuid)
        ndata = get_node_data({"uuid": self.uuid})
        #
        # expose properties
        # copy node group property data to the cooresponding node
        # rename the name to the original node name
        node_properties = ndata["properties"]
        for group_property in ndata["metadata"]["group_properties"]:
            node_name, prop_name, new_prop_name = group_property
            properties = nt.nodes[node_name].dbdata["properties"]
            properties[prop_name] = node_properties[new_prop_name]
            properties[prop_name]["name"] = prop_name
            # important to serialize
            nt.nodes[node_name].update_db_keys({"properties": serialize(properties)})
        # expose inputs
        node_group_inputs = ndata["inputs"]
        for group_input in ndata["metadata"]["group_inputs"]:
            node_name, input_name, new_input_name = group_input
            # find input of this node
            for node_group_input in node_group_inputs:
                if node_group_input["name"] == new_input_name:
                    links = node_group_input["links"]
            # find the input of the sub node in the nodetree
            sub_inputs = nt.nodes[node_name].dbdata["inputs"]
            for input in sub_inputs:
                if input["name"] == input_name:
                    input["links"] = links
            nt.nodes[node_name].update_db_keys({"inputs": sub_inputs})
            # update the properties of this input if it has a property
            if new_input_name in ndata["properties"]:
                properties = nt.nodes[node_name].dbdata["properties"]
                properties[input_name] = node_properties[new_input_name]
                properties[input_name]["name"] = input_name
                # important to serialize
                nt.nodes[node_name].update_db_keys(
                    {"properties": serialize(properties)}
                )
        nt.launch()
        return None
