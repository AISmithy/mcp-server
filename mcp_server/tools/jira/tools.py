import json
from mcp_server.registry import tool
from mcp_server.tools.jira.client import get_client


@tool("Jira")
def jira_list_projects(max_results: int = 50) -> str:
    """List all accessible Jira projects."""
    jira = get_client()
    projects = jira.projects()[:max_results]
    return json.dumps([
        {"key": p.key, "name": p.name, "id": p.id}
        for p in projects
    ], indent=2)


@tool("Jira")
def jira_search_issues(query: str, max_results: int = 20, start_at: int = 0) -> str:
    """Search Jira issues using JQL (Jira Query Language)."""
    jira = get_client()
    issues = jira.search_issues(query, maxResults=max_results, startAt=start_at)
    return json.dumps({
        "total": issues.total,
        "items": [
            {
                "key": i.key,
                "summary": i.fields.summary,
                "status": i.fields.status.name,
                "assignee": i.fields.assignee.displayName if i.fields.assignee else None,
                "priority": i.fields.priority.name if i.fields.priority else None,
                "issuetype": i.fields.issuetype.name,
                "created": i.fields.created,
                "updated": i.fields.updated,
            }
            for i in issues
        ],
    }, indent=2)


@tool("Jira")
def jira_get_issue(issue_key: str) -> str:
    """Get full details of a Jira issue."""
    jira = get_client()
    i = jira.issue(issue_key)
    return json.dumps({
        "key": i.key,
        "summary": i.fields.summary,
        "description": i.fields.description,
        "status": i.fields.status.name,
        "assignee": i.fields.assignee.displayName if i.fields.assignee else None,
        "reporter": i.fields.reporter.displayName if i.fields.reporter else None,
        "priority": i.fields.priority.name if i.fields.priority else None,
        "issuetype": i.fields.issuetype.name,
        "labels": i.fields.labels,
        "created": i.fields.created,
        "updated": i.fields.updated,
        "resolution": i.fields.resolution.name if i.fields.resolution else None,
    }, indent=2)


@tool("Jira")
def jira_create_issue(
    project_key: str,
    summary: str,
    issuetype: str = "Task",
    body: str = "",
    assignee: str = "",
    priority: str = "",
    labels: str = "",
) -> str:
    """Create a new Jira issue."""
    jira = get_client()
    fields: dict = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issuetype},
    }
    if body:
        fields["description"] = body
    if assignee:
        fields["assignee"] = {"name": assignee}
    if priority:
        fields["priority"] = {"name": priority}
    if labels:
        fields["labels"] = [s.strip() for s in labels.split(",") if s.strip()]
    issue = jira.create_issue(fields=fields)
    return json.dumps({"key": issue.key, "id": issue.id, "self": issue.self}, indent=2)


@tool("Jira")
def jira_update_issue(
    issue_key: str,
    summary: str = "",
    body: str = "",
    assignee: str = "",
    priority: str = "",
    labels: str = "",
) -> str:
    """Update fields of an existing Jira issue."""
    jira = get_client()
    issue = jira.issue(issue_key)
    fields: dict = {}
    if summary:
        fields["summary"] = summary
    if body:
        fields["description"] = body
    if assignee:
        fields["assignee"] = {"name": assignee}
    if priority:
        fields["priority"] = {"name": priority}
    if labels:
        fields["labels"] = [s.strip() for s in labels.split(",") if s.strip()]
    issue.update(fields=fields)
    return json.dumps({"key": issue_key, "updated": True}, indent=2)


@tool("Jira")
def jira_add_comment(issue_key: str, body: str) -> str:
    """Add a comment to a Jira issue."""
    jira = get_client()
    comment = jira.add_comment(issue_key, body)
    return json.dumps({"id": comment.id, "created": comment.created}, indent=2)


@tool("Jira")
def jira_list_transitions(issue_key: str) -> str:
    """List available workflow transitions for a Jira issue."""
    jira = get_client()
    transitions = jira.transitions(issue_key)
    return json.dumps([
        {"id": t["id"], "name": t["name"], "to": t["to"]["name"]}
        for t in transitions
    ], indent=2)


@tool("Jira")
def jira_transition_issue(issue_key: str, transition_id: str) -> str:
    """Transition a Jira issue to a new status using transition ID."""
    jira = get_client()
    jira.transition_issue(issue_key, transition_id)
    return json.dumps({"key": issue_key, "transitioned": True}, indent=2)
