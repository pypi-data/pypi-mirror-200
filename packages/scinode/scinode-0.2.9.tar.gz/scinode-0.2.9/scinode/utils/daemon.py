from scinode.database.client import scinodedb


def inspect_daemon_status(name, sleep=None):
    from scinode.utils.db import push_message
    import datetime
    import time

    if not sleep:
        data = scinodedb["daemon"].find_one({"name": name}, {"_id": 0, "sleep": 1})
        sleep = data["sleep"]
    push_message(name, f"{name},daemon,UPDATE")
    time.sleep(sleep)
    data = scinodedb["daemon"].find_one({"name": name}, {"_id": 0})
    data["lastUpdate"] = int(
        (datetime.datetime.utcnow() - data["lastUpdate"]).total_seconds()
    )
    running = data["lastUpdate"] < data["sleep"] * 1.5
    return data, running
