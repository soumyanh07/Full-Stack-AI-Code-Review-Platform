from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from app.core.config import settings


class CloneService:
    """
    Handles cloning GitHub repositories locally.
    """

    def __init__(self):
        self.storage_path = Path(settings.REPOSITORY_STORAGE)

        self.storage_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def clone_repository(
        self,
        repository_url: str,
        repository_name: str,
    ) -> str:
        """
        Clone a GitHub repository into local storage.

        Returns:
            Absolute path to the cloned repository.
        """

        repository_path = (
            self.storage_path / repository_name
        )

        # Remove previous clone if it exists
        if repository_path.exists():
            shutil.rmtree(repository_path)

        command = [
            "git",
            "clone",
            repository_url,
            str(repository_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to clone repository: "
                f"{result.stderr}"
            )

        return str(repository_path.resolve())