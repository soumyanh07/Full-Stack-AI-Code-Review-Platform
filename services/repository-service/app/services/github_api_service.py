from github import Github
import tempfile
import shutil
import subprocess
import os


class GitHubService:

    def clone_repository(self, repo_url: str):
        temp_dir = tempfile.mkdtemp()

        subprocess.run(
            [
                "git",
                "clone",
                repo_url,
                temp_dir,
            ],
            check=True,
        )

        return temp_dir

    def delete_repository(self, path: str):
        if os.path.exists(path):
            shutil.rmtree(path)


           