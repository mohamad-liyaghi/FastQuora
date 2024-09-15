from celery import Celery
from core.settings import settings

celery = Celery(__name__, broker=settings.CELERY_BROKER_URL)
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.autodiscover_tasks()
