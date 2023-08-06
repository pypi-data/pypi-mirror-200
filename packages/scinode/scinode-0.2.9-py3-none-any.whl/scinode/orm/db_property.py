import logging

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class DBProperty:
    """DBProperty Class.
    Object Relational Mapping for Property.

    uuid: str
        uuid of the node.
    name: str
        name of the node.

    Example:

    >>> # load property from data
    >>> property = DBProperty(node_uuid=node_uuid, name=name)
    """

    db_name: str = "node"

    def __init__(self, node_uuid=None, name=None) -> None:
        """init a instance

        Args:
            uuid (str, optional): uuid of the property.
                Defaults to None.
            dbdata (dict, optional): data of the property from database.
                Defaults to None.
        """
        self.node_uuid = node_uuid
        self.name = name
        self.record = self.dbdata

    @property
    def dbdata(self):
        """Item data from database

        Returns:
            dict: _description_
        """
        from scinode.database.client import scinodedb
        from scinode.utils.node import deserialize_item

        query = {"uuid": self.node_uuid}
        proj = {"properties": 1, "_id": 0}
        dbdata = scinodedb["node"].find_one(query, proj)["properties"]
        dbdata = deserialize_item(dbdata[self.name])
        return dbdata

    @property
    def uuid(self):
        return self.dbdata["uuid"]

    @property
    def value(self):
        return self.get_value()

    def get_value(self):
        """Get value of the property."""
        value = self.dbdata["value"]
        return value

    def __repr__(self) -> str:
        s = ""
        s += 'NodeProperty(name="{}")'.format(self.name)
        return s
