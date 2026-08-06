from app.core.celery_app import celery_app
from app.services.repository_sync_service import RepositorySyncService


@celery_app.task
def sync_repository(
    repository_id: int,
    repository_url: str,
):

    service = RepositorySyncService()

    return service.sync(
        repository_id,
        repository_url,
    )