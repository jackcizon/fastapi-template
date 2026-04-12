from celery import Celery
from src.core.config import Settings

dev_settings = Settings("dev")

broker_url = dev_settings.broker_url

app = Celery(main="fastapi_template_celery", broker=broker_url, backend=broker_url, result_expires=3600)

app.autodiscover_tasks(["tasks.email"])
