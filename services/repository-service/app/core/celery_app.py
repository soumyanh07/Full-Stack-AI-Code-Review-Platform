from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "repository_service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.tasks.index_repository",
        "app.tasks.review_pull_request",
        "app.tasks.dispatch_outbox",
    ],
)


celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "dispatch-indexing-outbox-every-30-seconds": {
        "task": "app.tasks.dispatch_outbox.dispatch_outbox_events",
        "schedule": 30.0,
    },
}
