from pathlib import Path

from git import Repo


class GitHubService:

    def clone_repository(
        self,
        url: str,
    ) -> str:

        repo_name = url.rstrip("/").split("/")[-1]

        clone_path = Path("repositories") / repo_name

        if clone_path.exists():
            return str(clone_path)

        Repo.clone_from(
            url,
            clone_path,
        )

        return str(clone_path)