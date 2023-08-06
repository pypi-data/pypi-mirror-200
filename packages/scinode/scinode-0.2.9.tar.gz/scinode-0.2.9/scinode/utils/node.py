import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def load_node(index):
    from scinode.database.client import scinodedb
    from scinode.orm.db_node import DBNode

    if isinstance(index, int):
        ndata = scinodedb["node"].find_one({"index": index}, {"_id": 0, "uuid": 1})
        node = DBNode(uuid=ndata["uuid"])
        return node
    elif isinstance(index, str):
        node = DBNode(uuid=index)
        return node


def get_executor(data):
    """Import executor from path and return the executor and type.
    If register is True, add the path to sys.path.
    """
    import importlib

    module = importlib.import_module("{}".format(data["path"]))
    executor = getattr(module, data["name"])
    type = data.get("type", "function")
    if data.get("register", False):
        import sys

        print("register", data["register"], "to sys.path")
        sys.path.append(data["register"])
    return executor, type


def get_node_data(query, proj={"_id": 0}):
    """Get node data from database.
    The properties are deserialized.
    """
    from scinode.database.client import scinodedb

    ndata = scinodedb["node"].find_one(query, proj)
    if ndata is None:
        return None
    for key in ["properties"]:
        if ndata.get(key):
            ndata[key] = deserialize(ndata[key])
    return ndata


def serialize(ndata):
    if isinstance(ndata, list):
        for i in range(len(ndata)):
            ndata[i] = serialize_item(ndata[i])
    else:
        for key, data in ndata.items():
            ndata[key] = serialize_item(data)
    return ndata


def deserialize(ndata):
    # print("deserialize", ndata)
    if isinstance(ndata, list):
        for i in range(len(ndata)):
            ndata[i] = deserialize_item(ndata[i])
    else:
        for key, data in ndata.items():
            ndata[key] = deserialize_item(data)
    return ndata


def serialize_item(data):
    import hashlib

    # print(f"serialize_item: {data}")
    Executor, _executor_type = get_executor(data["serialize"])
    data["value"] = Executor(data["value"])
    # could be json (str) or pickle binary
    if isinstance(data["value"], str):
        data["hash"] = hashlib.md5(data["value"].encode("utf-8")).hexdigest()
    else:
        data["hash"] = hashlib.md5(data["value"]).hexdigest()
    return data


def deserialize_item(data):
    # print("deserialize_item: ", data)
    Executor, _executor_type = get_executor(data["deserialize"])
    data["value"] = Executor(data["value"])
    return data


def yaml_to_dict(node):
    """Convert yaml data into dict."""
    metadata = node.get("metadata", {})
    metadata["identifier"] = node.pop("identifier")
    node["metadata"] = metadata
    # properties
    properties = {}
    if node.get("properties"):
        for name, p in node["properties"].items():
            properties[name] = {"value": p}
    node["properties"] = properties
    return node


def to_show_dict(node_full):
    # print("ntdata: ", ntdata)
    nd = {
        "identifier": node_full["metadata"]["identifier"],
        "name": node_full["name"],
        "uuid": node_full["uuid"],
        "state": node_full["state"],
        "action": node_full["action"],
        "description": node_full["description"],
        "metadata": {
            "daemon_name": node_full["metadata"]["daemon_name"],
        },
    }
    if node_full["metadata"]["node_type"].upper() == "REF":
        return nd
    # set node_full properties
    properties = node_full.get("properties")
    if properties:
        nd["properties"] = {}
        for name, p in properties.items():
            # udpate the properties
            if p["identifier"] in ["General"]:
                p["value"] = str(p["value"])
            nd["properties"][name] = p["value"]
    # inputs
    nd["inputs"] = []
    for input in node_full["inputs"]:
        for link in input["links"]:
            link["to_socket"] = input["name"]
            nd["inputs"].append(link)
    return nd


def to_edit_dict(node_full):
    # print("ntdata: ", ntdata)
    nd = {
        "identifier": node_full["metadata"]["identifier"],
        "name": node_full["name"],
        "uuid": node_full["uuid"],
        "state": node_full["state"],
        "action": node_full["action"],
        "description": node_full["description"],
        "metadata": {
            "daemon_name": node_full["metadata"]["daemon_name"],
        },
    }
    if node_full["metadata"]["node_type"].upper() == "REF":
        return nd
    # set node_full properties
    properties = node_full.get("properties")
    if properties:
        nd["properties"] = {}
        for name, p in properties.items():
            # udpate the properties
            if p["identifier"] not in ["General"]:
                nd["properties"][name] = p["value"]
    # inputs
    nd["inputs"] = []
    for input in node_full["inputs"]:
        for link in input["links"]:
            link["to_socket"] = input["name"]
            nd["inputs"].append(link)
    return nd


def get_input_socket_value(input, parameters=None):
    """Get input socket value.

    Args:
        input (dict): _description_
        parameters (dict): _description_

    Returns:
        dict: _description_
    """
    if not parameters:
        from scinode.database.client import scinodedb

        ndata = scinodedb["node"].find_one(
            {"uuid": input["node_uuid"]}, {"_id": 0, "properties": 1}
        )
        parameters = deserialize(ndata.get("properties"))
    # un-linked socket
    # print(input["links"])
    if len(input["links"]) == 0:
        logger.debug("un-linked socket")
        if input["name"] not in parameters:
            parameter = {"value": None, "hash": ""}
        else:
            parameter = parameters[input["name"]]
    elif len(input["links"]) == 1:
        # linked socket
        logger.debug("    single-linked socket")
        link = input["links"][0]
        results = get_data(query={"uuid": link["from_socket_uuid"]})
        # for special socket (e.g. Update), the result may not be avaible
        if results is None:
            parameter = {"value": None, "hash": ""}
        else:
            parameter = {"value": results["value"], "hash": results["hash"]}
    # check multi-input
    elif len(input["links"]) > 1:
        # linked socket
        logger.debug("    multi-linked socket")
        parameter = {"value": []}
        for link in input["links"]:
            results = get_data(query={"uuid": link["from_socket_uuid"]})
            value = results["value"] if results is not None else None
            # find the input socket based on socket name
            if isinstance(value, dict):
                parameter["value"].update(value)
            elif isinstance(value, list):
                parameter["value"].extend(value)
            else:
                parameter["value"].append(value)
    # print("Input {}".format(input["name"]), parameter)
    return parameter


def get_input_parameters_from_db(dbdata):
    """get node inputs from database

    The inputs are the outputs of parent nodes and
    the properties of the node itself.

    Returns:
        _type_: _description_
    """
    # get data of the node itself
    parameters = deserialize(dbdata.get("properties"))
    # get inputs sockets data
    inputs = dbdata.get("inputs")
    for input in inputs:
        result = get_input_socket_value(input, parameters)
        parameters[input["name"]] = result
    return parameters


def inspect_executor_arguments(parameters, args_keys, kwargs_keys):
    """Get the positional and keyword arguments

    Args:
        executor (_type_): _description_
        parameters (_type_): _description_
    """
    args = []
    kwargs = {}
    hash_parameters = {}
    for key in args_keys:
        args.append(parameters[key]["value"])
        hash_parameters[key] = parameters[key]["hash"]
    for key in kwargs_keys:
        kwargs[key] = parameters[key]["value"]
        hash_parameters[key] = parameters[key]["hash"]
    return args, kwargs, hash_parameters


def gather_node_results(ndata):
    from scinode.database.client import scinodedb

    outputs = ndata["outputs"]
    no = len(outputs)
    # init the results as a list
    for i in range(no):
        outputs[i]["value"] = []
    # fetch results from children
    children = scinodedb["node"].find(
        {"metadata.scattered_from": ndata["uuid"]},
        {"uuid": 1},
    )
    for child in children:
        child_results = get_results(child["uuid"])
        for i in range(no):
            value = child_results[i]["value"]
            outputs[i]["value"].append(value)
    return outputs


def get_result(uuid):
    from scinode.database.client import scinodedb
    from scinode.utils.node import deserialize_item

    query = {"uuid": uuid}
    data = scinodedb["data"].find_one(query, {"_id": 0})
    if data:
        result = deserialize_item(data)
    else:
        result = data
    return result


def get_results(uuid):
    """Get node results.

    If the node is scattered, gather the results.
    """
    from scinode.database.client import scinodedb

    ndata = scinodedb["node"].find_one(
        {"uuid": uuid}, {"outputs": 1, "metadata": 1, "name": 1, "uuid": 1}
    )
    ntdata = scinodedb["nodetree"].find_one(
        {"uuid": ndata["metadata"]["nodetree_uuid"]}, {f"nodes.{ndata['name']}": 1}
    )
    # check node is scattered or not
    if "scatter" in ntdata["nodes"][ndata["name"]]:
        results = gather_node_results(ndata)
    else:
        results = []
        for output in ndata["outputs"]:
            result = get_result(output["uuid"])
            results += [result]
    return results


def get_data(query):
    from scinode.database.db import scinodedb

    data = scinodedb["data"].find_one(query)
    # print("get_data: ", data)
    if data is None:
        return data
    data = deserialize_item(data)
    # print("get_data: ", data)
    return data


def write_log(uuid, log, database=True):
    from scinode.database.client import scinodedb

    if database:
        old_log = scinodedb["node"].find_one({"uuid": uuid}, {"_id": 0, "log": 1})[
            "log"
        ]
        log = old_log + log
        newvalues = {"$set": {"log": log}}
        scinodedb["node"].update_one({"uuid": uuid}, newvalues)


def save_socket_data(output):
    """save socket data to database.
    It is important to serialize the data."""
    from scinode.utils.db import replace_one
    from scinode.database.client import scinodedb

    output = serialize_item(output)
    replace_one(output, scinodedb["data"])


def expose_outputs(ndata):
    from scinode.orm.db_nodetree import DBNodeTree
    from scinode.engine.send_to_queue import send_message_to_queue
    from scinode.engine.config import broker_queue_name

    nt = DBNodeTree(uuid=ndata["uuid"])
    group_outputs = ndata["outputs"]
    no = len(group_outputs)
    # expose outputs
    for i in range(no):
        group_output = ndata["metadata"]["group_outputs"][i]
        node_name, socket_name, new_socket_name = group_output
        # find the output of the node in the nodetree
        outputs = nt.nodes[node_name].dbdata["outputs"]
        for output in outputs:
            if output["name"] == socket_name:
                result = nt.nodes[node_name].get_result(output["uuid"])
                group_outputs[i]["value"] = result["value"]
                save_socket_data(group_outputs[i])
    log = f"Node group: {ndata['name']} is exposed.\n"
    log += "Results: {}".format(group_outputs)
    #
    nodetree_uuid = ndata["metadata"]["nodetree_uuid"]
    node_name = ndata["name"]
    send_message_to_queue(
        broker_queue_name,
        f"{nodetree_uuid},node,{ndata['name']}:state:FINISHED",
    )
    print(f"  Node: {ndata['name']} is finished.\n")
    write_log(ndata["uuid"], log)


def save_node_results(dbdata, future_results):
    """Save node results to database."""
    from scinode.utils.node import write_log
    from scinode.engine.send_to_queue import send_message_to_queue
    from scinode.engine.config import broker_queue_name

    log = "\n    results from future: {}".format(future_results)
    outputs = dbdata["outputs"]
    no = len(outputs)
    nodetree_uuid = dbdata["metadata"]["nodetree_uuid"]
    # update results with the future_results
    if not isinstance(future_results, tuple):
        future_results = (future_results,)
    if len(future_results) != no:
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{dbdata['name']}:state:FAILED",
        )
        log += """xxxxxxxxxx Error xxxxxxxxxx\nNumber of results from future:
{} does not equal to number of sockets: {}.\n""".format(
            len(future_results), no
        )
        write_log(dbdata["uuid"], log)
        raise Exception(log)
    for i in range(no):
        outputs[i]["value"] = future_results[i]
        save_socket_data(outputs[i])
    write_log(dbdata["uuid"], log)


def calc_node_hash(dbdata, parameters_hash):
    import json
    import hashlib

    node_data = {
        "metadata": dbdata["metadata"]["hash"],
        "parameters": parameters_hash,
    }
    return hashlib.md5(json.dumps(node_data).encode("utf-8")).hexdigest()


def reuse_results_by_caching(ndata, cache_node):
    from scinode.engine.send_to_queue import send_message_to_queue
    from scinode.engine.config import broker_queue_name

    outputs = ndata["outputs"]
    no = len(outputs)
    # expose outputs
    for i in range(no):
        # find the output of the node in the nodetree
        result = get_result(cache_node["outputs"][i]["uuid"])
        if result is None:
            return 1
        outputs[i]["value"] = result["value"]
        save_socket_data(outputs[i])
    log = f"Node: {ndata['name']} reuse cache node {cache_node['name']} with uuid: {cache_node['uuid']}.\n"
    log += "Results: {}".format(outputs)
    #
    nodetree_uuid = ndata["metadata"]["nodetree_uuid"]
    send_message_to_queue(
        broker_queue_name,
        f"{nodetree_uuid},node,{ndata['name']}:state:FINISHED",
    )
    print(f"  Node: {ndata['name']} is finished.\n")
    write_log(ndata["uuid"], log)
    return 0


def get_node_constructor(ndata):
    """Get node constructor from node data.
    This will be used to re-create a node instance from other platforms.
    For example, from a web interface.
    """
    constructor = {
        "identifier": ndata["metadata"]["identifier"],
        "catalog": ndata["metadata"].get("catalog", "None"),
        "properties": [],
        "inputs": [],
        "outputs": [],
    }
    input_properties = []
    for input in ndata["inputs"]:
        inp = [input["identifier"], input["name"]]
        if input["name"] in ndata["properties"]:
            prop = ndata["properties"][input["name"]]
            input_properties.append(input["name"])
            prop = [prop["identifier"], prop["name"], prop["metadata"]]
            inp.append(prop)
        constructor["inputs"].append(inp)
    for output in ndata["outputs"]:
        constructor["outputs"].append([output["identifier"], output["name"]])
    for name, prop in ndata["properties"].items():
        # print("prop: ", prop)
        if name in input_properties:
            continue
        constructor["properties"].append(
            [prop["identifier"], prop["name"], prop["metadata"]]
        )
    return constructor


def node_shape(data):
    """_summary_

    Args:
        data (_type_): _description_


    =========
    |       o
    |       |
    |t      |
    |x      |
    o       |
    ========
    """
    pass


if __name__ == "__main__":
    uuid = ""
