from celery import Celery


app = Celery("fastapi_template_celery")
app.config_from_object("tasks.config")
app.autodiscover_tasks(["tasks.email"])
