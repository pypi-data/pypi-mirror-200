from celery import Task


class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        """
        retval – The return value of the task.
        task_id – Unique id of the executed task.
        args – Original arguments for the executed task.
        kwargs – Original keyword arguments for the executed task.
        """
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        exc – The exception raised by the task.
        task_id – Unique id of the failed task.
        args – Original arguments for the task that failed.
        kwargs – Original keyword arguments for the task that failed.
        """
        pass
