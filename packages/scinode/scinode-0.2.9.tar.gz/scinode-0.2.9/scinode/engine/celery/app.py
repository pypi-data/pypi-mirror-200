from celery import Celery

app = Celery("scinode", include=["scinode.engine.celery.tasks"])
app.config_from_object("scinode.engine.celery.celery_config")
