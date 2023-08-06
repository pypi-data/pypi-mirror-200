from scinode.database.db import ScinodeDB
import pandas as pd
from pprint import pprint
import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pd.set_option("display.max_rows", None)


class DataClient(ScinodeDB):
    """Class used to query and manipulate the database.

    Example:

    >>> client = DataClient()
    >>> client.list({"name": "math"})
    """

    def __init__(self) -> None:
        super().__init__()

    def list(self, query={}, column="", limit=100):
        """List node.

        Args:
            query (dict, optional): _description_. Defaults to {}.
            limit (int, optional): _description_. Defaults to 100.
        """
        projs = {
            "_id": 0,
            "index": 1,
            "name": 1,
            "identifier": 1,
        }
        column_name = ["index", "name", "identifier"]
        items = column.replace(" ", "").split(",") if column else []
        column_name += items
        for item in items:
            projs[f"value.{item}"] = 1
        # print(projs)
        data = self.db["data"].find(query, projs)
        new_data = []
        for d in data:
            # print(d)
            for item in items:
                d[item] = d["value"].pop(item)
            new_data.append(d)
        logger.debug(query)
        df = pd.DataFrame(new_data)
        if df.empty:
            print("index   name")
        else:
            df = df[-limit:]
            print(df[column_name])

    def show(self, query={}, all=False):
        """Show node data

        Args:
            query (dict, optional): _description_. Defaults to {}.
        """
        from scinode.utils.node import deserialize_item

        data = self.db["data"].find_one({"index": query["index"]}, {"_id": 0})
        if data is None:
            print("We can not find node with query: {}".format(query))
            return
        data = deserialize_item(data)
        if all:
            pprint(data)
        else:
            pprint(data["value"])


if __name__ == "__main__":
    d = DataClient()
    d.list()
    d.show({"index": 1})
