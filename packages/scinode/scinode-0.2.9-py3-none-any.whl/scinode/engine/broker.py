"""
"""
from scinode.database.client import scinodedb
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class Broker:
    """Broker Class.
    message-broker for SciNode.


    Example:

    >>> # load message
    >>> broker = Broker()
    >>> broker.process()
    >>> msg = broker.dbdata["msg"]
    """

    db_name: str = "broker"

    def __init__(self, name=None, pool=None, futures=None) -> None:
        """_summary_

        Args:
            name (_type_, optional): _description_. Defaults to None.
            pool (_type_, optional): _description_. Defaults to None.
        """
        self.name = name
        self.pool = pool
        self.futures = futures

    @property
    def dbdata(self):
        from scinode.database.client import scinodedb

        return scinodedb["broker"].find_one(
            {"name": self.name}, {"_id": 0, "msg": 1, "indices": 1}
        )

    @property
    def start(self):
        "Get the start of the new message"
        from scinode.database.client import scinodedb

        data = scinodedb["broker"].find_one(
            {"name": self.name}, {"_id": 0, "indices": {"$slice": -1}}
        )
        return data["indices"][0]

    def process_message(self):
        """apply message to nodetree and node"""
        start = self.start
        msgs = scinodedb["broker"].find_one(
            {"name": self.name}, {"_id": 0, "msg": {"$slice": [start, 1e6]}}
        )["msg"]
        # print("start: ", start)
        # print("msg: ", msg)
        nmsg = len(msgs)
        # print("apply_nodetree_message: ", bdata["nodetree"])
        if nmsg == 0:
            return
        from scinode.engine.engine import process_message

        for msg in msgs:
            process_message(msg, self.name, self.pool, self.futures)
            start += 1
            scinodedb["broker"].update_one(
                {"name": self.name}, {"$push": {"indices": start}}
            )

    def show(self):
        print("\n")
        print("Broker: ")
        print("-" * 40)
        data = self.dbdata
        print(data)
        n = len(data["indices"])
        for i in range(1, n):
            print("-" * 20)
            print(i - 1, i, "total: ", data["indices"][i] - data["indices"][i - 1])
            for m in data["msg"][data["indices"][i - 1] : data["indices"][i]]:
                uuid, catalog, msg = m.split(",")
                print(uuid, msg)
