from celery import Celery

celery_app = Celery(
    "testdebiritservice",
    broker="redis://redis:6379/0",
)

from testdebiritservice.tasks.fetch_prices import *

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "testdebiritservice.tasks.fetch_prices.fetch_prices",
        "schedule": 60.0,
    }
}

celery_app.conf.timezone = "UTC"