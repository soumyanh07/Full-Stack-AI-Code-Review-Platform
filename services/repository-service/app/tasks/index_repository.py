from app.core.celery_app import celery_app
from app.database.session import SessionLocal
from app.models.repository import Repository
from app.services.indexer_service import IndexerService


@celery_app.task
def index_repository(repository_id: int):
    """Load a registered repository and index it using its own storage path."""

    db = SessionLocal()

    try:
        repository = (
            db.query(Repository)
            .filter(Repository.id == repository_id)
            .first()
        )

        if repository is None:
            raise ValueError(
                f"Registered repository {repository_id} was not found."
            )

        repository_url = repository.url
        local_path = repository.local_path

        service = IndexerService()
        return service.index_repository(
            repository_id=repository_id,
            repository_url=repository_url,
            local_path=local_path,
        )
    finally:
        db.close()
