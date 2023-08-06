from scinode.daemon.base_daemon import BaseDaemon
from scinode.profile.profile import profile_datas
from scinode.engine.celery.app import app
import logging
import os
from pathlib import Path

home = Path.home()


class CeleryDaemon(BaseDaemon):
    def __init__(self, name, **kwargs) -> None:
        self.name = name
        self.logfile = os.path.join(
            home, ".scinode/daemon-{}-{}.log".format(profile_datas["name"], name)
        )
        self.concurrency = kwargs.get("concurrency", None)
        self.pool = kwargs.get("pool", None)
        self.loglevel = kwargs.get("loglevel", logging.INFO)
        self.queue = kwargs.get("queue", None)
        self.hostname = f"{self.name}@{profile_datas['computer']}"
        print(f"Celery worker: {self.name}")
        print(f"pool:        {self.pool}")
        print(f"concurrency: {self.concurrency}")

    def run(self):
        self.app = app
        worker = self.app.Worker(
            hostname=self.hostname,
            logfile=self.logfile,  # node format handled by celery.app.log.setup
            concurrency=self.concurrency,
        )
        worker.setup_defaults(
            pool=self.pool,
            loglevel=self.loglevel,
        )
        worker.setup_queues(self.queue)
        worker.start()

    @property
    def data(self):
        from scinode.database.client import scinodedb

        data = scinodedb["daemon"].find_one({"name": self.name})
        return data

    def get_pid(self):
        data = self.data
        pid = data.get("pid", 0)
        # print("name: {}, pid: {}".format(self.name, pid))
        return pid

    def inspect_status(self):
        from scinode.engine.celery.app import app

        reply = app.control.inspect()
        active = reply.active()
        if active is not None and self.hostname in active:
            data = active[self.hostname]
            running = True
            return data, running
        else:
            return {}, False
