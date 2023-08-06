import datetime
import os
import sys
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from scinode.daemon.base_daemon import BaseDaemon
from scinode.engine import MQ
from scinode.profile.profile import profile_datas
from scinode.utils.db import update_one

home = Path.home()


class ScinodeDaemon(BaseDaemon):
    """Daemon that fetch nodetree from database and call the
    engine to execute it.

    name: str
        Name of the daemon.
    pool: float
        Pool type: ThreadPoolExecutor, ProcessPoolExecutor
    concurrency: int
        Number of concurrency. Default 100 for ThreadPoolExecutor.
        4 for ProcessPoolExecutor.
    sleep: float
        Time interval to fetch data. Default 1.0

    """

    def __init__(self, name, pool="thread", concurrency=0, sleep=None):
        self.name = name
        self.sleep = sleep if sleep is not None else self.data["sleep"]
        self.pool = pool
        if pool.upper() in ["THREAD", "GEVENT", "EVENTLET"]:
            print("Use ThreadPoolExecutor.")
            self.Pool = ThreadPoolExecutor
            self.concurrency = concurrency if concurrency != 0 else 100
        elif pool.upper() in ["PREFORK", "PROCESS"]:
            print("Use ProcessPoolExecutor.")
            self.Pool = ProcessPoolExecutor
            self.concurrency = concurrency if concurrency != 0 else 4
        else:
            raise Exception("Pool type: {pool} is not supported.")
        logfile = os.path.join(
            home, ".scinode/daemon-{}-{}.log".format(profile_datas["name"], name)
        )
        super().__init__(logfile)
        # add sys path
        sys.path.append(os.path.join(profile_datas["config_path"], "custom_node"))

    def run(self):
        """Call engine to submit the job and collect the returned futures."""
        import time
        from scinode.database.client import scinodedb

        self.db = scinodedb
        self.update_data()
        #
        init_mq(self.name)
        # check the old process
        self.clean_old_process()
        self.futures = {}
        with self.Pool(max_workers=self.concurrency) as pool:
            mq = MQ(name=self.name, pool=pool, futures=self.futures)
            step = 0
            while True:
                print("{} {}".format(self.name, step))
                # --------------------------------------------------
                mq.process_message()
                # f.close()
                step += 1
                time.sleep(self.sleep)

    def clean_old_process(self):
        """Clean old process.

        When daemon is interupted, the old process is persist in a fake `running` state.
        """
        from scinode.orm.db_nodetree import DBNodeTree

        # query nodes
        query = {
            "action": {"$in": ["UPDATE", "NONE"]},
            "state": {"$in": ["RUNNING"]},
        }
        query["metadata.daemon_name"] = self.name
        ntdatas = list(
            self.db["nodetree"].find(
                query,
                {"name": 1, "uuid": 1, "nodes": 1},
            )
        )
        print("Reset: ")
        for ntdata in ntdatas:
            nt = DBNodeTree(uuid=ntdata["uuid"])  # , self.daemon_name)
            for name, node in ntdata["nodes"].items():
                if node["state"] == "RUNNING":
                    nt.reset_node(name, launch=True)
            nt.launch()

    def showlog(self, limit=100):
        with open(self.logfile) as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                print(line.strip())

    def update_data(self):
        """Update data in the database.
        - pid
        - concurrency
        - sleep
        """
        pid = os.getpid()
        data = {
            "name": self.name,
            "pid": pid,
            "concurrency": self.concurrency,
            "sleep": self.sleep,
            "lastUpdate": datetime.datetime.utcnow(),
        }
        # print("udpate: ", data)
        update_one(data, self.db["daemon"], key="name")
        # print("Write pid to database")

    def validate_name(self, name):
        from scinode.database.client import scinodedb

        data = scinodedb["daemon"].find_one({"name": name})
        if data is not None:
            return True
        else:
            print("Daemon {} is not setup.".format(name))
            return False

    @property
    def data(self):
        from scinode.database.client import scinodedb

        data = scinodedb["daemon"].find_one({"name": self.name})
        return data

    @property
    def lastUpdate(self):
        return self.get_lastUpdate()

    def get_lastUpdate(self):
        dt = (datetime.datetime.utcnow() - self.data["lastUpdate"]).total_seconds()
        return dt

    def get_pid(self):
        data = self.data
        pid = data.get("pid", 0)
        # print("name: {}, pid: {}".format(self.name, pid))
        return pid

    def inspect_status(self):
        from scinode.utils.daemon import inspect_daemon_status

        data, running = inspect_daemon_status(self.name)
        return data, running


def init_mq(name):
    """Init message queue."""
    from scinode.database.db import scinodedb

    data = scinodedb["mq"].find_one({"name": name})
    if not data:
        mq = {
            "name": name,
            "log": "",
            "msg": [],
            "indices": [0],
        }
        scinodedb["mq"].insert_one(mq)
        print("Init mq successfully!")


if __name__ == "__main__":
    daemon = ScinodeDaemon("localhost")
    daemon.start(daemonize=False)
