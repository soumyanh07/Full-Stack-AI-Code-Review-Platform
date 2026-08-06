from app.core.celery_app import celery_app
from app.services.indexer_service import IndexerService


@celery_app.task
def index_repository(
    repository_id: int,
    repository_url: str,
):

    service = IndexerService()

    return service.index_repository(
        repository_id,
        repository_url,
    )