from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.repository import Repository
from app.models.outbox_event import OutboxEvent
from app.schemas.repository import RepositoryCreate


class RepositoryService:
    """Owner-scoped repository operations."""

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def parse_github_url(url: str) -> tuple[str, str, str]:
        """Validate and canonicalize a public GitHub HTTPS repository URL."""

        try:
            parsed = urlsplit(url.strip())
        except ValueError as exc:
            raise ValueError("Invalid GitHub repository URL.") from exc

        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Invalid GitHub repository URL.") from exc

        if (
            parsed.scheme.lower() != "https"
            or (parsed.hostname or "").lower() != "github.com"
            or parsed.username is not None
            or parsed.password is not None
            or port not in (None, 443)
            or parsed.query
            or parsed.fragment
            or "%" in parsed.path
            or "\\\\" in parsed.path
        ):
            raise ValueError("Only HTTPS GitHub repository URLs are supported.")

        parts = [part for part in parsed.path.strip("/").split("/") if part]
        if len(parts) != 2:
            raise ValueError("URL must identify one GitHub owner and repository.")

        owner, repository = parts
        if repository.lower().endswith(".git"):
            repository = repository[:-4]

        valid_segment = re.compile(r"^[A-Za-z0-9_.-]{1,100}$")
        if (
            not valid_segment.fullmatch(owner)
            or not valid_segment.fullmatch(repository)
            or owner in {".", ".."}
            or repository in {".", ".."}
        ):
            raise ValueError("Invalid GitHub owner or repository name.")

        canonical_url = f"https://github.com/{owner}/{repository}.git"
        return owner, repository, canonical_url

    def get_repositories(self, owner_id: int) -> list[Repository]:
        return (
            self.db.query(Repository)
            .filter(Repository.owner_id == owner_id)
            .order_by(Repository.id.desc())
            .all()
        )

    def get_repository(self, repo_id: int, owner_id: int) -> Repository:
        repository = (
            self.db.query(Repository)
            .filter(
                Repository.id == repo_id,
                Repository.owner_id == owner_id,
            )
            .first()
        )
        if repository is None:
            raise ValueError("Repository not found.")
        return repository

    def get_registered_github_repositories(
        self,
        owner: str,
        repository: str,
    ) -> list[Repository]:
        """Resolve a GitHub webhook identity to every registered user copy."""

        matches = []
        rows = self.db.query(Repository).order_by(Repository.id.asc()).all()

        for row in rows:
            try:
                row_owner, row_repository, _ = self.parse_github_url(row.url)
            except ValueError:
                continue

            if (
                row_owner.casefold() == owner.casefold()
                and row_repository.casefold() == repository.casefold()
            ):
                matches.append(row)

        return matches

    def get_repository_by_github_identity(
        self,
        owner: str,
        repository: str,
        owner_id: int,
    ) -> Repository | None:
        rows = (
            self.db.query(Repository)
            .filter(Repository.owner_id == owner_id)
            .all()
        )
        for row in rows:
            try:
                row_owner, row_repository, _ = self.parse_github_url(row.url)
            except ValueError:
                continue
            if (
                row_owner.casefold() == owner.casefold()
                and row_repository.casefold() == repository.casefold()
            ):
                return row
        return None

    def create_repository(
        self,
        repository: RepositoryCreate,
        owner_id: int,
    ) -> Repository:
        owner, name, canonical_url = self.parse_github_url(repository.url)

        existing = (
            self.db.query(Repository)
            .filter(
                Repository.owner_id == owner_id,
                Repository.url == canonical_url,
            )
            .first()
        )
        if existing:
            raise ValueError("This repository is already registered.")

        storage_root = Path(settings.REPOSITORY_STORAGE).expanduser().resolve()

        db_repository = Repository(
            owner_id=owner_id,
            name=name,
            url=canonical_url,
            # Temporary non-empty value; replaced after the database assigns an ID.
            local_path=str(storage_root / "pending"),
        )

        try:
            self.db.add(db_repository)
            self.db.flush()

            # Isolate every registration, including registrations of the same
            # GitHub repository by different platform users.
            db_repository.local_path = str(
                (storage_root / str(db_repository.id)).resolve()
            )

            # Persist the indexing request in the same transaction.
            self.db.add(
                OutboxEvent(
                    repository_id=db_repository.id,
                    event_type="repository.index",
                )
            )

            self.db.commit()
            self.db.refresh(db_repository)
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("This repository is already registered.") from exc
        except Exception:
            self.db.rollback()
            raise

        return db_repository
