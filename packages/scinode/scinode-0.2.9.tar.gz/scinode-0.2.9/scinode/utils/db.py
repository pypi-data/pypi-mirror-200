def load(uuid, db="node"):
    from scinode.database.client import scinodedb

    data = scinodedb[db].find_one({"uuid": uuid})
    return data


def copy_item(name, item, db):
    """Copy one item in the collection

    Args:
        name (str): new name of the ite
        item (dict): data of the item
        db (collection): _description_
    """
    import uuid
    import copy

    data = copy.deepcopy(item)
    data.pop("_id")
    data["name"] = name
    uuid = str(uuid.uuid1())
    data["uuid"] = uuid
    insert_one(data, db)


def insert_one(item, db):
    """add one item to database

    Args:
        item (dict): _description_
    """
    if db.count_documents({}) == 0:
        index = 1
    else:
        index = db.find().sort("index", -1).limit(1)[0]["index"] + 1
    item.update({"index": index})
    db.insert_one(item)


def update_one(item, db, key="uuid"):
    """update one item to database

    Args:
        item (dict): _description_
    """
    query = {key: item[key]}
    newvalues = {"$set": item}
    db.update_one(query, newvalues)


def replace_one(item, db):
    """replace one item to database

    Args:
        item (dict): _description_
    """
    if db.find_one({"uuid": item["uuid"]}):
        update_one(item, db)
    else:
        insert_one(item, db)


def push_message(name, msg):
    """push msg to the broker.
    Args:
        data (dict): _description_
    """
    from scinode.database.client import scinodedb

    newvalues = {"$push": {"msg": msg}}
    # print("push message: ", newvalues)
    scinodedb["mq"].update_one({"name": name}, newvalues)


def push_messages(name, msgs):
    """push msgs to the message queue.
    Args:
        data (dict): _description_
    """
    from scinode.database.client import scinodedb

    newvalues = {"$push": {"msg": {"$each": msgs}}}
    # print("push message: ", newvalues)
    scinodedb["mq"].update_one({"name": name}, newvalues)


def write_log(query, log, db_name="node"):
    """Write log"""
    from scinode.database.client import scinodedb

    item = {"log": {"$concat": ["$log", log]}}
    scinodedb[db_name].update_one(query, [{"$set": item}])
