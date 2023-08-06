from scinode.orm import DBItem
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.config import broker_queue_name
import traceback
import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class EngineNode(DBItem):
    """EngineNode Class.
    Process the node with the data from the database.
    It can be called by the daemon or called manually.

    uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:
    >>> # load node data from database
    >>> query = {"uuid": "your-node-uuid"}
    >>> dbdata = scinodedb["node"].find_one(query)
    >>> node = EngineNode(uuid=dbdata["uuid"])  # , self.daemon_name)
    >>> future = node.process(pool, future)

    """

    db_name: str = "node"

    def __init__(self, uuid=None, dbdata=None, daemon_name="localhost") -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the node.
                Defaults to None.
            dbdata (dict, optional): data of the node from database.
                Defaults to None.
        """
        # print("Init Node Engine...")
        if dbdata:
            uuid = dbdata["uuid"]
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]
        self.daemon_name = daemon_name
        self.id = self.record["id"]
        self.nodetree_uuid = self.record["metadata"]["nodetree_uuid"]
        self.scattered_from = self.record["metadata"]["scattered_from"]
        self.scattered_label = self.record["metadata"]["scattered_label"]

    def process(self, pool, future=None, action=None):
        """process data based on the action flag.

        Args:
            pool (ThreadPoolExecutor): Pool used to submit job
            future (concurrent.futures.Future, optional): Defaults to None.

        Returns:
            oncurrent.futures.Future: _description_
        """
        print(f"Node Engine, process: {self.name}")
        try:
            future = self.apply_action(pool, future, action=action)
        except Exception:
            import traceback

            error = traceback.format_exc()
            log = "xxxxxxxxxx Failed xxxxxxxxxx\nNode {} failed due to: {}".format(
                self.name, error
            )
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)

        return future

    def apply_action(self, pool, future=None, action=None):
        """Apply node action

        Args:
            pool (dict): _description_
            future (future, optional): _description_. Defaults to None.
            action (_type_, optional): _description_. Defaults to None.

        Returns:
            future: _description_
        """
        if not action:
            action = self.record["action"]
        log = "\nDaemon: {}\n".format(self.daemon_name)
        log += "\nAction: {}\n".format(action)
        self.write_log(log)
        if action is None or action.upper() == "NONE":
            return
        elif action.upper() == "LAUNCH":
            future = self.launch(pool)
        elif action.upper() == "EXPOSE_OUTPUTS":
            self.expose_outputs()
            return None
        elif action.upper() == "CANCEL":
            self.cancel(future)
            return None
        else:
            log = "\nAction {} is not supported.".format(self.action)
            self.write_log(log)
        return future

    def launch(self, pool=None):
        """Launch node"""
        from scinode.database.client import scinodedb
        from scinode.utils.node import (
            get_input_parameters_from_db,
            inspect_executor_arguments,
            get_executor,
            calc_node_hash,
            reuse_results_by_caching,
        )

        # code here
        dbdata = self.record
        parameters = get_input_parameters_from_db(dbdata)
        # print("parameters: ", parameters)
        args, kwargs, hash_parameters = inspect_executor_arguments(
            parameters, dbdata["metadata"]["args"], dbdata["metadata"]["kwargs"]
        )
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
        scinodedb["node"].update_one({"uuid": self.uuid}, newvalues)
        # print("  Parameters: ", parameters)
        log = "args: {}\n".format(args)
        log += "kwargs: {}\n".format(kwargs)
        #
        if self.dbdata["executor"].get("register", False):
            import sys

            msg = f"register {self.dbdata['executor']['register']} to sys.path"
            sys.path.append(self.dbdata["executor"]["register"])
            log += msg
        self.write_log(log)
        Executor, executor_type = get_executor(self.dbdata["executor"])
        # print("  Executor: ", Executor)
        if executor_type.upper() == "CLASS":
            # For user defined node, we can add daemon name to kwargs
            executor = Executor(*args, dbdata=dbdata, **kwargs)
            future = pool.submit(executor.run)
        else:
            future = pool.submit(Executor, *args, **kwargs)
        msgs = f"{self.nodetree_uuid},node,{self.name}:state:RUNNING"
        send_message_to_queue(broker_queue_name, msgs)
        log = "\nNode is launched.\n"
        print("\nNode {} is launched.\n".format(dbdata["name"]))
        self.write_log(log)
        if dbdata["metadata"]["node_type"] != "GROUP":
            future.add_done_callback(self.check_future_done)

        return future

    def expose_outputs(self):
        """expose node group result from child nodes"""
        from scinode.utils.node import expose_outputs

        expose_outputs(self.dbdata)

    @property
    def input_node_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        from scinode.utils.node import get_input_node_data
        from scinode.database.client import db_node

        nodes = get_input_node_data(self.record, db_node)
        # print("Total: {} parent nodes.".format(len(nodes)))
        return nodes

    def check_future_done(self, future):
        """Check if node finished

        Args:
            future (_type_): _description_

        Raises:
            Exception: _description_
        """
        from scinode.utils.node import save_node_results

        log = "\n  Check result for Node: {}, {}.".format(self.id, self.name)
        if future.exception() is not None:
            error = future.exception()
            log += "\nxxxxxxxxxx Failed xxxxxxxxxx\nFuture with exception: {}".format(
                error
            )
            # self.state = "FAILED"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
            )
            self.update_db_keys({"error": str(error)})
            self.write_log(log)
            return
        elif future.cancelled():
            log == "\n  Job was cancelled"
            # self.state = "CANCELLED"
            # self.action = "NONE"
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            self.update_db_keys({"error": "Job was cancelled"})
            self.write_log(log)
            return
        else:
            # job is done, try to get result
            try:
                future_results = future.result()
                save_node_results(self.dbdata, future_results)
                msgs = f"{self.nodetree_uuid},node,{self.name}:state:FINISHED"
                send_message_to_queue(broker_queue_name, msgs)
            except Exception:
                error = traceback.format_exc()
                log += "\nxxxxxxxxxx Failed xxxxxxxxxx\nFetch results from future failed, due to: {}".format(
                    error
                )
                # self.state = "FAILED"
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                self.update_db_keys({"error": str(error)})
                self.write_log(log)
                return

    def __repr__(self) -> str:
        s = ""
        s += 'EngineNode(name="{}", uuid="{}", nodetree_uuid = {},\
state={}, action={})'.format(
            self.name,
            self.uuid,
            self.nodetree_uuid,
            self.state,
            self.action,
        )
        return s

    def write_log(self, log, daemon=False, database=True):
        from scinode.utils.db import write_log

        if daemon:
            print(log)
        if database:
            write_log({"uuid": self.uuid}, log, "node")
