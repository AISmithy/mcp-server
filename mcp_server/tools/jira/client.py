import os
from jira import JIRA


def get_client() -> JIRA:
    url = os.environ.get("JIRA_URL")
    username = os.environ.get("JIRA_USERNAME")
    token = os.environ.get("JIRA_API_TOKEN")
    if not all([url, username, token]):
        raise RuntimeError(
            "JIRA_URL, JIRA_USERNAME, and JIRA_API_TOKEN environment variables are required."
        )
    return JIRA(server=url, basic_auth=(username, token))
