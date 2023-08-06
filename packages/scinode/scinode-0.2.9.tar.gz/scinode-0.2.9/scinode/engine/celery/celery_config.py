from scinode.profile.profile import profile_datas

broker_url = profile_datas["broker_url"]
# Backend Settings
result_backend = profile_datas["db_address"]
mongodb_backend_settings = {
    "database": profile_datas["db_name"],
    "taskmeta_collection": "celery_task",
}
task_track_started = True
