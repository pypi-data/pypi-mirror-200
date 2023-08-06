"""
"""
from scinode.orm import DBItem
from scinode.engine.node_engine import EngineNode
from scinode.engine.send_to_queue import send_message_to_queue
from scinode.engine.config import broker_queue_name
from scinode.database.client import db_node, scinodedb
import time
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class EngineNodeTree(DBItem):
    """EngineNodeTree Class.
    Process the nodetree with the data from the database.
    It can be called by the daemon or called manually.

    uuid: str
        uuid of the nodetree.

    Example:

    >>> # load nodetree data from database
    >>> query = {"uuid": "your-nodetree-uuid"}
    >>> dbdata = scinodedb["nodetree"].find_one(query)
    >>> nodetree = EngineNodeTree(uuid=dbdata["uuid"])
    >>> nodetree.process()
    """

    db_name: str = "nodetree"

    def __init__(self, uuid=None) -> None:
        """_summary_

        Args:
            uuid (_type_, optional): _description_. Defaults to None.
            dbdata (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(uuid)
        self.record = self.dbdata
        self.name = self.record["name"]

    def update_nodetree_state(self):
        """process the nodetree from database.
        1) analyze_node_state
        2) analyze_nodetree_state
        3) push message
        """
        from scinode.engine.send_to_queue import send_message_to_queue

        try:
            # skip paused nodetree
            if self.record["state"] in ["PAUSED"]:
                return
            # analysze node states
            node_states = self.analyze_node_state()
            # update nodetree state
            state, action = self.analyze_nodetree_state(node_states)
            send_message_to_queue(
                broker_queue_name, f"{self.uuid},nodetree,state:{state}"
            )
        except Exception:
            import traceback

            error = traceback.format_exc()
            print(
                "xxxxxxxxxx Failed xxxxxxxxxx\nNode {} failed due to: {}".format(
                    self.name, error
                )
            )
            self.update_db_keys({"state": "FAILED"})
            self.update_db_keys({"action": "NONE"})
            self.update_db_keys({"error": str(error)})

    def apply_nodetree_state(self, state):
        """Apply state to nodetree"""
        from scinode.engine.send_to_queue import expose_outputs

        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {"state": state}}
        )
        if self.record["metadata"]["parent_node"] != "":
            ndata = scinodedb["node"].find_one(
                {"uuid": self.uuid}, {"name": 1, "metadata": 1}
            )
            if state == "FINISHED":
                print(f"nodetree {self.name} is finished.")
                expose_outputs(
                    ndata["metadata"]["daemon_name"],
                    ndata["metadata"]["nodetree_uuid"],
                    ndata["name"],
                )
            else:
                msgs = f"{ndata['metadata']['nodetree_uuid']},node,{ndata['name']}:state:{state}"
                send_message_to_queue(broker_queue_name, msgs)

    def apply_nodetree_action(self, action):
        """Apply action to nodetree"""
        tstart = time.time()
        # print(f"Nodetree action: {action}")
        if action.upper() == "UPDATE":
            self.update_nodetree_state()
        elif action.upper() == "LAUNCH":
            self.launch_nodetree()
        elif action.upper() == "PAUSE":
            self.pause_nodetree()
        elif action.upper() == "PLAY":
            self.play_nodetree()
        elif action.upper() == "CANCEL":
            self.cancel_nodetree()
        elif action.upper() == "RESET":
            self.reset_nodetree()
        else:
            print("Action {} is not supported.".format(action))
        logger.debug("apply_nodetree_action, time: {}".format(time.time() - tstart))

    def launch_nodetree(self):
        """Launch nodetree."""
        print(f"Launch nodetree: {self.uuid}")
        send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:RUNNING")
        self.update_nodetree_state()

    def pause_nodetree(self):
        """Pause nodetree."""
        print(f"Pause nodetree: {self.uuid}")
        send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:PAUSED")

    def play_nodetree(self):
        """Play nodetree."""
        print(f"Play nodetree: {self.uuid}")
        send_message_to_queue(broker_queue_name, f"{self.uuid},nodetree,state:RUNNING")

    def reset_nodetree(self):
        """Reset node and all its child nodes.

        Args:
            name (str): name of the node to be paused
        """
        print(f"Reset nodetree: {self.uuid}")
        ntdata = scinodedb["nodetree"].find_one({"uuid": self.uuid}, {"nodes": 1})
        for name in ntdata["nodes"]:
            ntdata["nodes"][name]["state"] = "CREATED"
        # print("update_node_state: ", ntdata["nodes"])
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {"nodes": ntdata["nodes"]}}
        )

    def cancel_nodetree(self):
        """Cancel nodetree."""
        print(f"Cancel nodetree: {self.uuid}")
        # print("update_node_state: ", ntdata["nodes"])
        scinodedb["nodetree"].update_one(
            {"uuid": self.uuid}, {"$set": {"state": "CANCELLED"}}
        )

    def analyze_node_state(self):
        """Analyze node states.

        - check if node is ready (input nodes finished)
        - if one node fails, is cancelled or is paused, change
            all its children nodes to hanging.

        """
        from scinode.engine.send_to_queue import launch_node

        # "FINISHED",  "CANCELLED",  "FAILED",  "RUNNING",  "PAUSED",  "CREATED",  "WAITING",  "SKIPPED",  "UNKNOWN"
        # fake state: "HANGING"
        #
        node_states = {}
        for name, dbdata in self.record["nodes"].items():
            node_states[name] = dbdata["state"]
        #
        #
        # update node will ignore the "Update" socket for the first run
        states = {}
        for name, ndata in self.record["nodes"].items():
            if ndata["node_type"] in ["REF"]:
                continue
            # check parent nodes
            if node_states[name] in ["CREATED", "WAITING"]:
                ready = self.check_parent_state(name)
                if ready:
                    states.update({f"nodes.{name}.state": "READY"})
                    launch_node(ndata["daemon"], self.uuid, name)
            elif node_states[name] in ["SCATTERED"]:
                state, action = self.check_scattered_state(name)
                if state == "FINISHED":
                    msgs = f"{self.uuid},node,{name}:state:FINISHED"
                    send_message_to_queue(broker_queue_name, msgs)
                elif state == "FAILED":
                    msgs = f"{self.uuid},node,{name}:state:FINISHED"
                    send_message_to_queue(broker_queue_name, msgs)
            # update child nodes
            if ndata["state"] in ["FAILED", "SKIPPED", "CANCELLED"]:
                children = self.record["connectivity"]["child_node"][name]
                for c in children:
                    node_states[c] = "HANGING"
        if states:
            scinodedb["nodetree"].update_one({"uuid": self.uuid}, {"$set": states})
        # print(f"analyze_node_state, push: {msgs}")
        # logger.debug("analyze_node_state, time: {}".format(time.time() - tstart))
        return node_states

    def analyze_nodetree_state(self, node_states):
        """analyze nodetree state

        Args:
            node_states (_type_): _description_
        """
        states = list(node_states.values())
        state_list = [
            "CREATED",
            "READY",
            "FINISHED",
            "FAILED",
            "PAUSED",
            "SKIPPED",
            "RUNNING",
            "WAITING",
            "SCATTERED",
            "CANCELLED",
        ]

        counts = {x: states.count(x) for x in state_list}
        s = ""
        # s += "    Created: {}, Ready: {}, FINISHED: {}, Failed: {}, Paused: {}, Skipped: {}, Running: {}, Waiting: {}, Scattered: {}, Cancelled: {}\n".format(
        s += "{:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d} {:4d}\n".format(
            counts["CREATED"],
            counts["READY"],
            counts["RUNNING"],
            counts["FINISHED"],
            counts["FAILED"],
            counts["PAUSED"],
            counts["SKIPPED"],
            counts["WAITING"],
            counts["SCATTERED"],
            counts["CANCELLED"],
        )
        log = "{}".format(s)
        self.write_log(log)
        # get nodetree state
        if (
            counts["CREATED"] == 0
            and counts["READY"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] == 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FINISHED"
            action = "NONE"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] != 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FAILED"
            action = "NEED_HELP"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["PAUSED"] == 0
            and counts["CANCELLED"] != 0
        ):
            state = "CANCELLED"
            action = "NEED_HELP"
        else:
            state = "RUNNING"
            action = "UPDATE"
        # logger.debug("analyze_nodetree_state, time: {}".format(time.time() - tstart))
        return state, action

    @property
    def dbdata_nodes(self):
        """Fetch node data from database
        1) node belong to this nodetree
        2) reference node used in this nodetree

        Returns:
            dict: node data from database
        """
        query = {"metadata.nodetree_uuid": self.dbdata["uuid"]}
        project = {"_id": 0, "uuid": 1, "name": 1, "state": 1, "action": 1}
        datas = list(db_node.find(query, project))
        dbdata_nodes = {data["name"]: data for data in datas}
        # find the ref nodes
        ref_nodes = [
            node["name"]
            for node in self.record["nodes"].values()
            if node["node_type"] == "REF"
        ]
        # populate the ref nodes
        for name in ref_nodes:
            query = {"uuid": self.record["nodes"][name]["uuid"]}
            data = db_node.find_one(query, project)
            dbdata_nodes[name] = data

        return dbdata_nodes

    def cancel(self):
        dbdata_nodes = self.dbdata_nodes
        for name, dbdata in dbdata_nodes.items():
            node = EngineNode(dbdata)
            node.update_db_keys({"action": "CANCEL"})
        self.action = "NONE"

    def check_parent_state(self, name):
        """Check parent states

        Args:
            name (str): name of node to be check

        Returns:
            ready (bool): ready to launch or not
        """
        ready = True
        # control node needs special treatment.
        # update node will ingore the "Update" socket for the first run
        inputs = self.record["connectivity"]["input_node"][name]
        # print("node_type: ", self.record["nodes"][name]["node_type"])
        if self.record["nodes"][name]["node_type"] == "Update":
            record = db_node.find_one(
                {"uuid": self.record["nodes"][name]["uuid"]},
                {"_id": 0, "metadata.counter": 1},
            )
            counter = record["metadata"]["counter"]
            print("counter: ", counter)
            if counter == 0:
                inputs.pop("Update", None)
        # scatter node will always ingore the "Stop" socket
        elif self.record["nodes"][name]["node_type"] == "Scatter":
            inputs.pop("Stop", None)
        #
        for socke_name, input_nodes in inputs.items():
            for input_node_name in input_nodes:
                if self.record["nodes"][input_node_name]["node_type"] == "REF":
                    # find ref_uuid
                    uuid = self.record["nodes"][input_node_name]["uuid"]
                    data = scinodedb["node"].find_one({"uuid": uuid}, {"metadata": 1})
                    ref_uuid = data["metadata"]["ref_uuid"]
                    # find ref date
                    data = scinodedb["node"].find_one({"uuid": ref_uuid}, {"name": 1})
                    ref_name = data["name"]
                    data = scinodedb["nodetree"].find_one(
                        {f"nodes.{ref_name}.uuid": ref_uuid},
                        {f"nodes.{ref_name}.state": 1},
                    )
                    # print(f"input_node_name: {input_node_name}, ref_uuid: {ref_uuid}, state: {data['state']}")
                    self.record["nodes"][input_node_name]["state"] = data["nodes"][
                        ref_name
                    ]["state"]
                if self.record["nodes"][input_node_name]["state"] != "FINISHED":
                    ready = False
                    return ready
        return ready

    def check_scattered_state(self, name):
        """Check scattered states

        Args:
            name (str): name of node to be check
            dbdata_nodes (dict): data of all nodes

        Returns:
            ready (bool): ready to launch or not
        """
        state = "SCATTERED"
        action = "GATHER"
        node_states = self.record["nodes"][name]["scatter"]
        s = ""
        states = list(node_states.values())
        state_list = [
            "CREATED",
            "READY",
            "FINISHED",
            "FAILED",
            "PAUSED",
            "SKIPPED",
            "RUNNING",
            "WAITING",
            "SCATTERED",
            "CANCELLED",
        ]

        counts = {x: states.count(x) for x in state_list}
        s = ""
        s += "    Created: {}, Ready: {}, FINISHED: {}, Failed: {}, Paused: {}, Skipped: {}, Running: {}, Waiting: {}, Scattered: {}, Cancelled: {}\n".format(
            counts["CREATED"],
            counts["READY"],
            counts["FINISHED"],
            counts["FAILED"],
            counts["PAUSED"],
            counts["SKIPPED"],
            counts["RUNNING"],
            counts["WAITING"],
            counts["SCATTERED"],
            counts["CANCELLED"],
        )
        if (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] == 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FINISHED"
            action = "NONE"
            print(
                f"    \nCheck scattered node: {name}, state: {state}, action: {action}"
            )
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["FAILED"] != 0
            and counts["PAUSED"] == 0
            and counts["WAITING"] == 0
            and counts["SCATTERED"] == 0
        ):
            state = "FAILED"
            action = "NEED_HELP"
        elif (
            counts["CREATED"] == 0
            and counts["RUNNING"] == 0
            and counts["PAUSED"] == 0
            and counts["CANCELLED"] != 0
        ):
            state = "CANCELLED"
            action = "NEED_HELP"

        return state, action

    def load_nodes(self):
        dbdata_nodes = self.dbdata_nodes
        nodes = {}
        for name, dbdata in dbdata_nodes.items():
            node = EngineNode(uuid=dbdata["uuid"])  # , self.daemon_name)
            nodes[node.name] = node
        self.nodes = nodes

    def write_log(self, log, daemon=False, database=True):
        from scinode.utils.db import write_log

        if daemon:
            print(log)
        if database:
            write_log({"uuid": self.uuid}, log, "nodetree")
