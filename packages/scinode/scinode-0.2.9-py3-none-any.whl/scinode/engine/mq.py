"""
"""
from scinode.database.client import scinodedb
import logging


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class MQ:
    """MQ Class.
    message-queue for SciNode.


    Example:

    >>> # load message
    >>> mq = MQ()
    >>> mq.process()
    >>> msg = mq.dbdata["msg"]
    """

    db_name: str = "mq"

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

        return scinodedb[self.db_name].find_one(
            {"name": self.name}, {"_id": 0, "msg": 1, "indices": 1}
        )

    @property
    def start(self):
        "Get the start of the new message"
        from scinode.database.client import scinodedb

        data = scinodedb[self.db_name].find_one(
            {"name": self.name}, {"_id": 0, "indices": {"$slice": -1}}
        )
        return data["indices"][0]

    def process_message(self):
        """apply message to nodetree and node"""
        start = self.start
        msgs = scinodedb[self.db_name].find_one(
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
            exit_code = process_message(msg, self.name, self.pool, self.futures)
            start += 1
            scinodedb[self.db_name].update_one(
                {"name": self.name}, {"$push": {"indices": start}}
            )

    def show(self, limit=1e9):
        print("\n")
        print(f"Message qeuue: {self.name}")
        print("-" * 40)
        data = self.dbdata
        n = len(data["indices"])
        start = max(1, n - limit)
        for i in range(start, n):
            print(i - 1, i, "total: ", data["indices"][i] - data["indices"][i - 1])
            for m in data["msg"][data["indices"][i - 1] : data["indices"][i]]:
                uuid, catalog, msg = m.split(",")
                print(uuid, catalog, msg)
        print(
            "\nTo be processed: {}".format(len(data["msg"][data["indices"][n - 1] :]))
        )
        print(data["msg"][data["indices"][n - 1] :])
