import json
from base64 import b64decode
from mcp_server.registry import tool
from mcp_server.tools.github.client import get_client


@tool("GitHub")
def github_search_repositories(query: str, page: int = 1, per_page: int = 10) -> str:
    """Search for GitHub repositories."""
    g = get_client()
    results = g.search_repositories(query=query)
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, repo in enumerate(results):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({
            "full_name": repo.full_name,
            "description": repo.description,
            "html_url": repo.html_url,
            "stars": repo.stargazers_count,
            "language": repo.language,
            "updated_at": str(repo.updated_at),
        })
    return json.dumps({"total_count": results.totalCount, "items": items}, indent=2)


@tool("GitHub")
def github_get_repository(owner: str, repo: str) -> str:
    """Get detailed information about a GitHub repository."""
    g = get_client()
    r = g.get_repo(f"{owner}/{repo}")
    return json.dumps({
        "full_name": r.full_name,
        "description": r.description,
        "html_url": r.html_url,
        "stars": r.stargazers_count,
        "forks": r.forks_count,
        "open_issues": r.open_issues_count,
        "language": r.language,
        "default_branch": r.default_branch,
        "created_at": str(r.created_at),
        "updated_at": str(r.updated_at),
        "topics": r.get_topics(),
        "license": r.license.name if r.license else None,
        "visibility": r.visibility,
    }, indent=2)


@tool("GitHub")
def github_list_issues(
    owner: str, repo: str, state: str = "open",
    labels: str = "", page: int = 1, per_page: int = 20,
) -> str:
    """List issues in a GitHub repository."""
    g = get_client()
    r = g.get_repo(f"{owner}/{repo}")
    kwargs: dict = {"state": state}
    if labels:
        kwargs["labels"] = [r.get_label(l.strip()) for l in labels.split(",")]
    issues = r.get_issues(**kwargs)
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, issue in enumerate(issues):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({
            "number": issue.number,
            "title": issue.title,
            "state": issue.state,
            "html_url": issue.html_url,
            "user": issue.user.login if issue.user else None,
            "labels": [lb.name for lb in issue.labels],
            "created_at": str(issue.created_at),
        })
    return json.dumps(items, indent=2)


@tool("GitHub")
def github_get_issue(owner: str, repo: str, issue_number: int) -> str:
    """Get details of a specific GitHub issue."""
    g = get_client()
    issue = g.get_repo(f"{owner}/{repo}").get_issue(number=issue_number)
    return json.dumps({
        "number": issue.number,
        "title": issue.title,
        "state": issue.state,
        "body": issue.body,
        "html_url": issue.html_url,
        "user": issue.user.login if issue.user else None,
        "labels": [lb.name for lb in issue.labels],
        "created_at": str(issue.created_at),
        "updated_at": str(issue.updated_at),
    }, indent=2)


@tool("GitHub")
def github_create_issue(
    owner: str, repo: str, title: str,
    body: str = "", labels: str = "", assignees: str = "",
) -> str:
    """Create a new issue in a GitHub repository."""
    g = get_client()
    r = g.get_repo(f"{owner}/{repo}")
    kwargs: dict = {"title": title}
    if body:
        kwargs["body"] = body
    if labels:
        kwargs["labels"] = [s.strip() for s in labels.split(",") if s.strip()]
    if assignees:
        kwargs["assignees"] = [s.strip() for s in assignees.split(",") if s.strip()]
    issue = r.create_issue(**kwargs)
    return json.dumps({"number": issue.number, "html_url": issue.html_url}, indent=2)


@tool("GitHub")
def github_list_pull_requests(
    owner: str, repo: str, state: str = "open", page: int = 1, per_page: int = 20,
) -> str:
    """List pull requests in a GitHub repository."""
    g = get_client()
    pulls = g.get_repo(f"{owner}/{repo}").get_pulls(state=state)
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, pr in enumerate(pulls):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "html_url": pr.html_url,
            "user": pr.user.login if pr.user else None,
            "head": pr.head.ref,
            "base": pr.base.ref,
            "draft": pr.draft,
        })
    return json.dumps(items, indent=2)


@tool("GitHub")
def github_get_pull_request(owner: str, repo: str, pull_number: int) -> str:
    """Get details of a specific GitHub pull request."""
    g = get_client()
    pr = g.get_repo(f"{owner}/{repo}").get_pull(number=pull_number)
    return json.dumps({
        "number": pr.number,
        "title": pr.title,
        "state": pr.state,
        "body": pr.body,
        "html_url": pr.html_url,
        "head": pr.head.ref,
        "base": pr.base.ref,
        "merged": pr.merged,
        "additions": pr.additions,
        "deletions": pr.deletions,
        "changed_files": pr.changed_files,
    }, indent=2)


@tool("GitHub")
def github_get_file_contents(owner: str, repo: str, path: str, ref: str = "") -> str:
    """Get file or directory contents from a GitHub repository."""
    g = get_client()
    r = g.get_repo(f"{owner}/{repo}")
    kwargs: dict = {"path": path}
    if ref:
        kwargs["ref"] = ref
    contents = r.get_contents(**kwargs)
    if isinstance(contents, list):
        return json.dumps([{"name": c.name, "path": c.path, "type": c.type} for c in contents], indent=2)
    if contents.encoding == "base64" and contents.content:
        return b64decode(contents.content).decode("utf-8")
    return json.dumps({"name": contents.name, "path": contents.path}, indent=2)


@tool("GitHub")
def github_list_branches(owner: str, repo: str, page: int = 1, per_page: int = 30) -> str:
    """List branches in a GitHub repository."""
    g = get_client()
    branches = g.get_repo(f"{owner}/{repo}").get_branches()
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, b in enumerate(branches):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({"name": b.name, "sha": b.commit.sha, "protected": b.protected})
    return json.dumps(items, indent=2)


@tool("GitHub")
def github_list_commits(
    owner: str, repo: str, sha: str = "", path: str = "",
    page: int = 1, per_page: int = 20,
) -> str:
    """List commits in a GitHub repository."""
    g = get_client()
    kwargs: dict = {}
    if sha:
        kwargs["sha"] = sha
    if path:
        kwargs["path"] = path
    commits = g.get_repo(f"{owner}/{repo}").get_commits(**kwargs)
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, c in enumerate(commits):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({
            "sha": c.sha[:7],
            "message": c.commit.message,
            "author": c.commit.author.name if c.commit.author else None,
            "date": str(c.commit.author.date) if c.commit.author else None,
            "html_url": c.html_url,
        })
    return json.dumps(items, indent=2)


@tool("GitHub")
def github_search_code(query: str, page: int = 1, per_page: int = 10) -> str:
    """Search for code across GitHub repositories."""
    g = get_client()
    results = g.search_code(query=query)
    per_page = min(per_page, 100)
    start = (page - 1) * per_page
    items = []
    for i, item in enumerate(results):
        if i < start:
            continue
        if i >= start + per_page:
            break
        items.append({
            "name": item.name,
            "path": item.path,
            "repository": item.repository.full_name,
            "html_url": item.html_url,
        })
    return json.dumps({"total_count": results.totalCount, "items": items}, indent=2)
