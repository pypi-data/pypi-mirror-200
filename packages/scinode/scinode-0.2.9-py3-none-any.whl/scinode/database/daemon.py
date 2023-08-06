from scinode.database.db import ScinodeDB
from pprint import pprint
import datetime
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pd.set_option("display.max_rows", 200)


class DaemonClient(ScinodeDB):
    """Class used to query and manipulate the database."""

    def __init__(self) -> None:
        super().__init__()

    def get_data(self, query={}):
        data = list(self.db["daemon"].find(query))
        return data

    def get_daemon(self, name, computer):
        """Get daemon data by name"""
        data = self.get_data()
        for d in data:
            if d["name"] == name and d["computer"] == computer:
                return d
        return None

    def list(self, query={}):
        """List daemon"""
        data = self.get_data(query)
        df = pd.DataFrame(data)
        if df.empty:
            print(
                "index",
                "name",
                "computer",
                "workdir",
                "pid",
                "worker",
            )
        else:
            print(
                df[
                    [
                        "index",
                        "name",
                        "computer",
                        "workdir",
                        "pid",
                        "worker",
                    ]
                ]
            )

    def show(self, query={}):
        data = self.db["daemon"].find_one(query)
        if data is None:
            print("We can not find daemon with query: {}".format(query))
            return
        pprint(data)

    def status(self, query={}):
        """Get daemon status.
        - First send a message to mq to check the daemon status.
        - Daemon recieve the message and update the lastUpdate field in the database.
        - Wait sleep time.
        - Get the lastUpdate time
        """
        from colorama import Fore, Style
        from scinode.utils.daemon import inspect_daemon_status

        data = list(self.db["daemon"].find(query))
        if data is None:
            print("We can not find daemon with query: {}".format(query))
            return
        print(
            "{:10s} {:5s} {:5s} {:10s}".format("name", "sleep", "lastUpdate", "running")
        )
        for d in data:
            new_data, running = inspect_daemon_status(d["name"], d["sleep"])
            d["lastUpdate"] = new_data["lastUpdate"]
            if running:
                d["running"] = Fore.GREEN + str(running) + Style.RESET_ALL
            else:
                d["running"] = Fore.RED + str(running) + Style.RESET_ALL
            print(
                "{:10s} {:5.1f} {:10d} {:10s}".format(
                    d["name"], d["sleep"], d["lastUpdate"], d["running"]
                )
            )


if __name__ == "__main__":
    d = DaemonClient()
    d.list()
    d.show({"index": 1})
