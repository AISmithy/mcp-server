import os
from github import Github, Auth


def get_client() -> Github:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN environment variable is required.")
    return Github(auth=Auth.Token(token))
