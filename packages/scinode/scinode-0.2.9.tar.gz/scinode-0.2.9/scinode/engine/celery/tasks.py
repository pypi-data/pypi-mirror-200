"""
TODO pass default daemon seting to task, e.g. work_dir
"""
from scinode.utils.node import get_results, write_log
from scinode.engine.celery.app import app
from scinode.engine.config import broker_queue_name
from scinode.profile.profile import profile_datas
import traceback
import sys, os

sys.path.append(os.path.join(profile_datas["config_path"], "custom_node"))


@app.task
def get_daemon_status():
    """should broadcast to all daemon"""
    pass


@app.task
def process_message(msg):
    from scinode.engine.engine import Engine

    en = Engine()
    en.process(msg)
    return None


@app.task
def launch_nodetree(uuid):
    from scinode.engine.nodetree_engine import EngineNodeTree

    en = EngineNodeTree(uuid)
    en.launch_nodetree()
    return None


@app.task
def launch_node(nodetree_uuid, node_name):
    """Launch node"""
    from scinode.utils.node import (
        get_input_parameters_from_db,
        inspect_executor_arguments,
        get_executor,
        calc_node_hash,
        reuse_results_by_caching,
    )
    from scinode.database.client import scinodedb
    from scinode.engine.send_to_queue import send_message_to_queue
    from scinode.utils.node import save_node_results

    # get node data
    ntdata = scinodedb["nodetree"].find_one(
        {"uuid": nodetree_uuid}, {f"nodes.{node_name}": 1, "metadata.daemon_name": 1}
    )
    ntdata["uuid"] = nodetree_uuid
    node_uuid = ntdata["nodes"][node_name]["uuid"]
    dbdata = scinodedb["node"].find_one({"uuid": node_uuid})
    log = ""
    try:
        parameters = get_input_parameters_from_db(dbdata)
        # print("parameters: ", parameters)
        args, kwargs, hash_parameters = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], dbdata["metadata"]["kwargs"]
        )
        #
        node_hash = calc_node_hash(dbdata, hash_parameters)
        if dbdata["metadata"].get("use_cache", False):
            # match hash
            cache_node = scinodedb["node"].find_one(
                {"hash": node_hash}, {"_id": 0, "name": 1, "uuid": 1, "outputs": 1}
            )
            if cache_node is not None:
                # msgs = f"{nodetree_uuid},node,{node_name}:action:CACHING"
                # send_message_to_queue(broker_queue_name, msgs)
                exit_code = reuse_results_by_caching(dbdata, cache_node)
                if exit_code == 0:
                    return
        newvalues = {"$set": {"hash": node_hash}}
        scinodedb["node"].update_one({"uuid": node_uuid}, newvalues)
        # print("  Parameters: ", parameters)
        log += "args {} \n".format(args)
        log += "kwargs {} \n".format(kwargs)
        Executor, executor_type = get_executor(dbdata["executor"])
    except Exception as error:
        error = traceback.format_exc()
        log += "\nxxxxxxxxxx Failed xxxxxxxxxx\n{}".format(error)
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{node_name}:state:FAILED",
        )
        write_log(node_uuid, log)
        return
    msgs = f"{nodetree_uuid},node,{node_name}:state:RUNNING"
    send_message_to_queue(broker_queue_name, msgs)
    try:
        if executor_type.upper() == "CLASS":
            # For user defined node, we can add daemon name to kwargs
            executor = Executor(
                *args,
                **kwargs,
                dbdata=dbdata,
            )
            future = executor.run()
        else:
            future = Executor(*args, **kwargs)
        if dbdata["metadata"]["node_type"] == "GROUP":
            msgs = f"{nodetree_uuid},node,{node_name}:state:RUNNING"
        else:
            save_node_results(dbdata, future)
            msgs = f"{nodetree_uuid},node,{node_name}:state:FINISHED"
        log += "\nNode is finished"
        print("\nNode: {} is finished".format(dbdata["name"]))
        write_log(node_uuid, log)
        send_message_to_queue(broker_queue_name, msgs)
    except Exception as error:
        error = traceback.format_exc()
        log += "\nxxxxxxxxxx Failed xxxxxxxxxx\n{}".format(error)
        # self.state = "FAILED"
        send_message_to_queue(
            broker_queue_name,
            f"{nodetree_uuid},node,{node_name}:state:FAILED",
        )
        write_log(node_uuid, log)


@app.task
def expose_outputs(nodetree_uuid, node_name):
    """Expose node group results.
    Outgoing connections to the the Group Output will become
    attached to the output sockets of
    coresponding nodes.
    """
    from scinode.database.client import scinodedb
    from scinode.utils.node import expose_outputs

    # get node uuid
    print(f"Expose outputs for node group {node_name}\n")
    ntdata = scinodedb["nodetree"].find_one(
        {"uuid": nodetree_uuid}, {f"nodes.{node_name}": 1, "metadata.daemon_name": 1}
    )
    # get node data
    node_uuid = ntdata["nodes"][node_name]["uuid"]
    ndata = scinodedb["node"].find_one({"uuid": node_uuid})
    expose_outputs(ndata)


if __name__ == "__main__":
    import logging

    worker = app.Worker()
    worker.setup_defaults(loglevel=logging.INFO)
    worker.setup_queues("localhost")
    worker.start()
