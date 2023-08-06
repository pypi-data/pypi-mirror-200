from scinode.database.db import ScinodeDB
import pandas as pd
from pprint import pprint
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


pd.set_option("display.max_rows", None)


class NodetreeClient(ScinodeDB):
    """Class used to query and manipulate the database.

    Example:

    >>> client = NodeTreeClient()
    >>> client.list({"name": "math"})
    """

    def __init__(self) -> None:
        super().__init__()

    def delete(self, query):
        nodetrees = self.db["nodetree"].find(query)
        count_node = 0
        count_data = 0
        for nodetree in nodetrees:
            nodes = self.db["node"].find(
                {"metadata.nodetree_uuid": nodetree["uuid"]}, {"_id": 0, "uuid": 1}
            )
            # delete the data (output results)
            for node in nodes:
                resutls = self.db["data"].delete_many({"node_uuid": node["uuid"]})
                count_data += resutls.deleted_count
            # delete the nodes
            resutls = self.db["node"].delete_many(
                {"metadata.nodetree_uuid": nodetree["uuid"]}
            )
            count_node += resutls.deleted_count
        resutls = self.db["nodetree"].delete_many(query)
        print(
            "{} nodetree are deleted.\n{} node are deleted.\n{} data are deleted.".format(
                resutls.deleted_count, count_node, count_data
            )
        )

    def list(self, query={}, limit=100):
        """List nodetree.

        Args:
            query (dict, optional): _description_. Defaults to {}.
            limit (int, optional): _description_. Defaults to 100.
        """
        from scinode.utils import get_time
        from colorama import Fore, Style

        data = self.db["nodetree"].find(
            query,
            {
                "_id": 0,
                "index": 1,
                "name": 1,
                "state": 1,
                "action": 1,
                "lastUpdate": 1,
                "metadata": 1,
            },
        )
        if data is None:
            print("We can not find nodetree with query: {}".format(query))
            return
        new_data = []
        for d in data:
            dt = int((datetime.datetime.utcnow() - d["lastUpdate"]).total_seconds())
            d["lastUpdate_second"] = dt
            d["lastUpdate"] = get_time(dt)
            # color print
            if d["state"] == "FINISHED":
                d["state"] = Fore.GREEN + d["state"] + Style.RESET_ALL
            if d["state"] == "CREATED":
                d["state"] = Fore.LIGHTBLUE_EX + d["state"] + Style.RESET_ALL
            elif d["state"] == "FAILED":
                d["state"] = Fore.RED + d["state"] + Style.RESET_ALL
            elif d["state"] == "RUNNING":
                d["state"] = Fore.YELLOW + d["state"] + Style.RESET_ALL
            new_data.append(d)
        print(
            "{:5s} {:20s} {:10s} {:10s} {:10s}".format(
                "index", "name", "state", "action", "lastUpdate"
            )
        )
        if new_data:
            for d in new_data:
                print(
                    "{:5d} {:20s} {:<10s} {:<10s} {:10s}".format(
                        d["index"],
                        d["name"][0:20],
                        d["state"],
                        d["action"],
                        d["lastUpdate"],
                    )
                )

    def show(self, query, broker=False, all=False):
        """Show nodetree data.

        Args:
            query (_type_): _description_
        """
        data = self.db["nodetree"].find_one({"index": query["index"]}, {"log": 0})
        if data is None:
            print("We can not find nodetree with query: {}".format(query))
            return
        print("-" * 60)
        print("\nNodeTree:")
        print("name: {}\nuuid: {}\n".format(data["name"], data["uuid"]))
        data["generation_time"] = data.get("_id").generation_time
        if all:
            pprint(data)
        query = {"metadata.nodetree_uuid": data["uuid"]}
        self.show_nodes(data["uuid"], data["nodes"])
        if broker:
            self.show_broker(data["uuid"])
        print("-" * 60)

    def show_nodes(self, uuid, nodes):
        from colorama import Fore, Style

        dbnodes = list(
            self.db["node"].find(
                {"metadata.nodetree_uuid": uuid}, {"name": 1, "index": 1}
            )
        )
        print("-" * 60)
        print("Nodes: \n")
        print("{:10s} {:15s} {:10s} {:10s}".format("index", "name", "state", "action"))
        print("{:10s} {:15s} {:10s} {:10s}".format("-----", "----", "-----", "------"))
        for node in dbnodes:
            state = nodes[node["name"]]["state"]
            if nodes[node["name"]]["state"] == "FINISHED":
                state = Fore.GREEN + nodes[node["name"]]["state"] + Style.RESET_ALL
            elif nodes[node["name"]]["state"] == "FAILED":
                state = Fore.RED + nodes[node["name"]]["state"] + Style.RESET_ALL
            elif nodes[node["name"]]["state"] == "RUNNING":
                state = Fore.YELLOW + nodes[node["name"]]["state"] + Style.RESET_ALL
            print(
                "{:^10d} {:15s} {:10s} {:10s}".format(
                    node["index"],
                    node["name"],
                    state,
                    nodes[node["name"]]["action"],
                )
            )

    def get_full_data(self, query):
        from scinode.utils.nodetree import get_nt_full_data

        data = get_nt_full_data(query)
        return data

    def get_yaml_data(self, query):
        import yaml
        from scinode.utils.nodetree import to_edit_dict

        ndata = self.get_full_data(query)
        data = to_edit_dict(ndata)
        s = yaml.dump(data, sort_keys=False)
        return s, ndata

    def log(self, query):
        """Show the execution log of this nodetree.

        Args:
            query (_type_): _description_
        """
        data = self.db["nodetree"].find_one(
            {"index": query["index"]}, {"_id": 0, "log": 1, "name": 1, "uuid": 1}
        )
        if data is None:
            print("We can not find nodetree with query: {}".format(query))
            return
        print("Nodetree: {}, {}".format(data["name"], data["uuid"]))
        print(data["log"])


if __name__ == "__main__":
    d = NodetreeClient()
    d.list()
    d.show({"index": 1})
