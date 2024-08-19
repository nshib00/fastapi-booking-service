from celery import Celery

from app.config import settings


celery = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['fastapi_course_app.app.tasks.tasks'],
)