"""
"""
from scinode.engine import EngineNodeTree
from scinode.engine import EngineNode
from scinode.database.client import scinodedb
from scinode.engine.config import broker_queue_name
from scinode.engine.send_to_queue import send_message_to_queue
import traceback
import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def update_node_group(func):
    def wrapper(self, name, **kwargs):
        if self.record["nodes"][name]["node_type"] == "REF":
            raise Exception("Can not change state of a reference node")
        return func(self, name, **kwargs)

    return wrapper


class Engine:
    """Engine Class.

    Example:

    >>> en = Engine()
    >>> en.process()
    """

    def __init__(self, name=None, pool=None, futures=None) -> None:
        """_summary_

        Args:
            name (_type_, optional): _description_. Defaults to None.
            pool (_type_, optional): _description_. Defaults to None.
        """
        self.name = name
        self.pool = pool
        self.futures = futures

    def process(self, msg):
        """apply message to nodetree and node"""
        print(f"process: {msg}")
        try:
            uuid, catalog, body = msg.split(",")
        except Exception as e:
            print(e)
            return 1
        if catalog == "nodetree":
            try:
                self.apply_nodetree_message(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {"error": str(error)}}
                )
        elif catalog == "node":
            try:
                self.apply_node_message(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(error)
                )
                data = msg.split(":")
                name = data[0]
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "FAILED"}}
                )
                scinodedb["nodetree"].update_one(
                    {"uuid": uuid}, {"$set": {f"nodes.{name}.error": str(error)}}
                )
        elif catalog == "daemon":
            try:
                self.apply_daemon_action(uuid, body)
            except Exception as e:
                error = traceback.format_exc()
                print(
                    "xxxxxxxxxx Failed xxxxxxxxxx\n Failed due to: \n{}".format(
                        str(error)
                    )
                )
        else:
            raise Exception(f"Unknown type {catalog}")

        return 0

    def apply_nodetree_message(self, uuid, msg):
        # print("apply_nodetree_message: ", msg)
        key, value = msg.split(":")
        # print(name, m)
        nodetree = EngineNodeTree(uuid=uuid)
        if key == "action":
            nodetree.apply_nodetree_action(value)
        elif key == "state":
            nodetree.apply_nodetree_state(value)

    def apply_node_message(self, uuid, msg):
        """apply action to all nodes"""
        from scinode.database.client import scinodedb
        from scinode.utils.db import write_log
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        # print(f"apply_node_message: {msg}")
        data = msg.split(":")
        if len(data) == 3:
            name, key, value = data
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.{key}": value}}
            )
            # push message to child node
            ntdata = scinodedb["nodetree"].find_one(
                {"uuid": uuid}, {f"nodes.{name}.uuid": 1}
            )
            node_uuid = ntdata["nodes"][name]["uuid"]
            # print(f"node uuid: {node_uuid}, {key}: {value}")
            child_nodes = scinodedb["node"].find(
                {"metadata.ref_uuid": node_uuid}, {"metadata": 1, "name": 1}
            )
            if child_nodes is not None:
                for child in child_nodes:
                    msg = f"{child['metadata']['nodetree_uuid']},node,{name}:{key}:{value}"
                    send_message_to_queue(broker_queue_name, msg)
            # push message to parent nodetree
            if key == "state" and value not in ["RUNNING"]:
                self.update_nodetree_state(uuid)
                record = scinodedb["nodetree"].find_one({"uuid": uuid}, {"metadata": 1})
                if record["metadata"]["scatter_node"]:
                    send_message_to_queue(
                        broker_queue_name,
                        f"{record['metadata']['parent']},node,scatter:{record['metadata']['scattered_label']}:{msg}",
                    )
            if key == "action":
                self.apply_node_action(uuid, name, value)
        elif len(data) == 5:
            key1, label, name, key2, value = data
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.{key1}.{label}": value}}
            )
            self.update_nodetree_state(uuid)
        write_log({"metadata.nodetree_uuid": uuid, "name": name}, f"\n{msg}\n", "node")
        # logger.debug("apply_node_message, time: {}".format(time.time() - tstart))

    def apply_node_action(self, uuid, name, action):
        tstart = time.time()
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"apply_node_action: {name}, {action}")
        if action == "NONE":
            scinodedb["nodetree"].update_one(
                {"uuid": uuid}, {"$set": {f"nodes.{name}.action": "NONE"}}
            )
        elif action == "LAUNCH":
            self.launch_node(uuid, name)
        elif action == "EXPOSE_OUTPUTS":
            self.expose_outputs(uuid, name)
        elif action == "PAUSE":
            self.pause_node(uuid, name)
        elif action == "PLAY":
            self.play_node(uuid, name)
        elif action == "SKIP":
            self.skip_node(uuid, name)
        elif action == "RESET":
            self.reset_node(uuid, name)
        elif action == "RESET_LAUNCH":
            self.reset_node(uuid, name, launch=True)
        elif action == "FINISH":
            # TODO
            # self.record[name]["state"] = "FINISHED"
            pass
        # print("apply_node_action: ", self.record["nodes"])
        logger.debug("apply_node_action, time: {}".format(time.time() - tstart))

    def launch_node(self, uuid, name):
        """Launch node"""
        print(f"\nLaunch node: {name}, {uuid}")
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        node = EngineNode(uuid=ntdata["nodes"][name]["uuid"], daemon_name=self.name)
        future = node.process(self.pool, self.futures.get(uuid), action="LAUNCH")
        self.futures[uuid] = future

    def expose_outputs(self, uuid, name):
        """Expose node group outputs."""
        print(f"\n Expose node group: {name}")
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        node = EngineNode(uuid=ntdata["nodes"][name]["uuid"], daemon_name=self.name)
        future = node.process(
            self.pool, self.futures.get(uuid), action="EXPOSE_OUTPUTS"
        )
        self.futures[uuid] = future

    def update_nodetree_state(self, uuid):
        """update nodetree state.

        If there is a node change its state, we need to call this funciton.
        """
        # print("\nUpdate nodetree: {}".format(uuid))
        nodetree = EngineNodeTree(uuid=uuid)
        nodetree.update_nodetree_state()
        del nodetree

    def pause_node(self, uuid, name):
        """Pause node.

        Args:
            name (str): name of the node to be paused
        """
        logger.debug("pause node, name: {}".format(name))
        ndata = scinodedb["nodetree"].find_one({"uuid": uuid}, {f"nodes.{name}": 1})
        if ndata["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{ndata['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "PAUSED"}}
        )

    def play_node(self, uuid, name):
        """Play node.

        Args:
            name (str): name of the node to be played
        """
        logger.debug("play node, name: {}".format(name))
        ndata = scinodedb["nodetree"].find_one({"uuid": uuid}, {f"nodes.{name}": 1})
        if ndata["nodes"][name]["node_type"] == "GROUP":
            send_message_to_queue(
                broker_queue_name,
                f"{ndata['nodes'][name]['uuid']},nodetree,action:PAUSED",
            )
        scinodedb["nodetree"].update_one(
            {"uuid": uuid}, {"$set": {f"nodes.{name}.state": "CREATED"}}
        )

    def skip_node(self, uuid, name):
        """Skip node.

        Args:
            name (str): name of the node to be skiped
        """
        nodes_to_skip = []
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"connectivity.child_node": 1}
        )
        child_nodes = ntdata["connectivity"]["child_node"][name]
        nodes_to_skip.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_skip:
            items[f"nodes.{name}.state"] = "SKIPPED"
        scinodedb["nodetree"].update_one({"uuid": uuid}, {"$set": items})

    def reset_node(self, uuid, name, launch=False):
        """Reset node and all its child nodes.

        Args:
            name (str): name of the node to be paused
        """
        nodes_to_reset = [name]
        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"connectivity.child_node": 1}
        )
        child_nodes = ntdata["connectivity"]["child_node"][name]
        nodes_to_reset.extend(child_nodes)
        logger.debug("reset node, name: {}".format(name))
        items = {}
        for name in nodes_to_reset:
            items[f"nodes.{name}.state"] = "CREATED"
        if launch:
            for name in nodes_to_reset:
                items[f"nodes.{name}.action"] = "LAUNCH"
        scinodedb["nodetree"].update_one({"uuid": uuid}, {"$set": items})

    def cancel(self, uuid, name):
        """Cancel node"""
        from scinode.engine.config import broker_queue_name
        from scinode.engine.send_to_queue import send_message_to_queue

        ntdata = scinodedb["nodetree"].find_one(
            {"uuid": uuid}, {"_id": 0, f"nodes.{name}": 1}
        )
        uuid = ntdata["nodes"][name]["uuid"]
        future = self.futures.get(uuid)
        if future is not None:
            log = "Node is running: {}.\n".format(future.running())
            was_calcelled = future.cancel()
            if was_calcelled:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
                )
                log += "Node is cancelled: {}".format(was_calcelled)
                # self.update_db_keys({"outputs": {}})
            else:
                send_message_to_queue(
                    broker_queue_name,
                    f"{self.nodetree_uuid},node,{self.name}:state:FAILED",
                )
                log += "Can not cancel node.".format()
        else:
            send_message_to_queue(
                broker_queue_name,
                f"{self.nodetree_uuid},node,{self.name}:state:CANCELLED",
            )
            log = "Future is None. Node {} is not running. Can not cancel.".format(
                self.dbdata["name"]
            )
        self.write_log(log)

    def apply_daemon_action(self, name, action):
        # print("apply_node_action: ", self.record["nodes"])
        # print(f"{action} {name}")
        print(f"apply_daemon_action: {name}, {action}")
        if action == "STOP":
            self.stop_daemon(name)
        elif action == "UPDATE":
            self.update_daemon(name)
        elif action == "RESTART":
            self.restart_daemon(name)

    def update_daemon(self, name):
        from scinode.utils.db import update_one
        import datetime

        update_one(
            {"name": name, "lastUpdate": datetime.datetime.utcnow()},
            scinodedb["daemon"],
            key="name",
        )

    def stop_daemon(self, name):
        from scinode.daemon.daemon import ScinodeDaemon

        print(f"Sotp daemon {name}...")
        scinodedb["mq"].update_one(
            {"name": name}, {"$set": {"msg": [], "indices": [0]}}
        )
        daemon = ScinodeDaemon(name)
        daemon.stop()

    def restart_daemon(self, name):
        import os

        print(f"Restart daemon {name}...")
        scinodedb["mq"].update_one(
            {"name": name}, {"$set": {"msg": [], "indices": [0]}}
        )
        os.system("scinode daemon hard-restart")

    def write_log(self, log, daemon=False, database=True):
        if daemon:
            print(log)
        if database:
            old_log = self.db.find_one({"uuid": self.uuid}, {"_id": 0, "log": 1})["log"]
            log = old_log + log
            self.update_db_keys({"log": log})

    def push_db_keys(self, items={}):
        """update data and state to database"""
        query = {"uuid": self.uuid}
        newvalues = {"$push": items}
        self.db.update_one(query, newvalues)


def process_message(msgs, name, pool=None, futures=None):
    en = Engine(name=name, pool=pool, futures=futures)
    exit_code = en.process(msgs)
    return exit_code
