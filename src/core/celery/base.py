from celery import Celery
from celery.schedules import crontab
from core.settings import settings

celery = Celery(__name__, broker=settings.CELERY_BROKER_URL)
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.autodiscover_tasks(["app.tasks"])

celery.conf.beat_schedule = {
    "auto_insert_vote_from_cache_to_db": {
        "task": "app.tasks.vote.auto_insert_vote_from_cache_to_db",
        "schedule": crontab(minute="*/1"),
    }
}
