import shutil
from pathlib import Path

from git import Repo


class GitHubService:

    CLONE_DIRECTORY = Path("repositories")

    def clone_repository(self, url: str):

        self.CLONE_DIRECTORY.mkdir(exist_ok=True)

        repository_name = url.rstrip("/").split("/")[-1]

        destination = self.CLONE_DIRECTORY / repository_name

        if destination.exists():
            shutil.rmtree(destination)

        Repo.clone_from(url, destination)

        return str(destination)