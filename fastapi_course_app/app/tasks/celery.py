from app.config import settings
from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ],
    broker_connection_retry_on_startup=True,
)


celery.conf.beat_schedule = {
    "booking_1_day": {
        "task": "booking_1_day",
        "schedule": crontab(hour="9", minute="0"),
    },
    "booking_3_day": {
        "task": "booking_3_days",
        "schedule": crontab(hour="15", minute="30"),
    },
}
