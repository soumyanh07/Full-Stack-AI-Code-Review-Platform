from datetime import datetime, timezone

from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.models.outbox_event import OutboxEvent
from app.tasks.index_repository import index_repository


@celery_app.task
def dispatch_outbox_events(batch_size: int = 50):
    """Publish pending indexing events without losing failed deliveries."""

    db = SessionLocal()
    dispatched = 0
    failed = 0

    try:
        events = (
            db.query(OutboxEvent)
            .filter(
                OutboxEvent.dispatched_at.is_(None),
                OutboxEvent.event_type == "repository.index",
            )
            .order_by(OutboxEvent.created_at.asc(), OutboxEvent.id.asc())
            .with_for_update(skip_locked=True)
            .limit(batch_size)
            .all()
        )

        for event in events:
            event.attempts += 1
            try:
                index_repository.apply_async(args=[event.repository_id])
                event.dispatched_at = datetime.now(timezone.utc)
                event.last_error = None
                dispatched += 1
            except Exception as exc:
                event.last_error = str(exc)[:2000]
                failed += 1

        db.commit()
        return {"dispatched": dispatched, "failed": failed}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
