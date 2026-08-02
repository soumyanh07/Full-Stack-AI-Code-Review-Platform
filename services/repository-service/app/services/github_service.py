import os
import shutil
import stat
from pathlib import Path

from git import Repo


class GitHubService:

    CLONE_DIRECTORY = Path("repositories")

    @staticmethod
    def _remove_readonly(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def clone_repository(self, url: str):

        self.CLONE_DIRECTORY.mkdir(exist_ok=True)

        repository_name = url.rstrip("/").split("/")[-1]

        destination = self.CLONE_DIRECTORY / repository_name

        if destination.exists():
            shutil.rmtree(destination, onerror=self._remove_readonly)

        Repo.clone_from(url, destination)

        return str(destination)