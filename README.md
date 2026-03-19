# MCP Server Hub

A Python-based [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes tools for multiple integrations — GitHub, Jira, REST API, Oracle, and MongoDB — for use by AI assistants.

## Prerequisites

- Python 3.10+
- Credentials for the integrations you want to use (see [Configuration](#configuration))

## Installation

```bash
pip install -e .
```

## Browser UI

Start the server in SSE mode and open the browser UI to explore and test all tools interactively:

```bash
python -m mcp_server --sse
```

Then open: **http://localhost:8000/ui**

Tools are grouped by integration in the sidebar. Select a tool, fill in the parameters, and click **Run**.

## Configuration

Each integration is activated by setting its environment variables. Integrations without credentials are gracefully skipped at startup.

### GitHub

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Jira

```bash
export JIRA_URL="https://your-org.atlassian.net"
export JIRA_USERNAME="you@example.com"
export JIRA_API_TOKEN="your_api_token"
```

### REST API

```bash
export REST_API_BASE_URL="https://api.example.com"
export REST_API_TOKEN="your_token"           # optional
export REST_API_TOKEN_HEADER="Authorization" # optional, default: Authorization
export REST_API_TOKEN_PREFIX="Bearer"        # optional, default: Bearer
```

### Oracle Database

```bash
export ORACLE_USER="your_user"
export ORACLE_PASSWORD="your_password"
export ORACLE_DSN="host:port/service_name"
```

### MongoDB

```bash
export MONGODB_URI="mongodb://localhost:27017"
export MONGODB_DATABASE="your_database"
```

On Windows (PowerShell), use `$env:VAR = "value"` syntax.

## Usage

### Run directly (stdio — for MCP clients)

```bash
mcp-server-hub
```

### Run with browser UI (SSE mode)

```bash
mcp-server-hub --sse
# or
python -m mcp_server --sse
```

### VS Code / Copilot

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "hub": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here",
        "JIRA_URL": "https://your-org.atlassian.net",
        "JIRA_USERNAME": "you@example.com",
        "JIRA_API_TOKEN": "your_api_token",
        "MONGODB_URI": "mongodb://localhost:27017",
        "MONGODB_DATABASE": "your_database"
      }
    }
  }
}
```

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hub": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

## Available Tools

### GitHub (11 tools)

| Tool | Description |
|---|---|
| `github_search_repositories` | Search for GitHub repositories |
| `github_get_repository` | Get detailed info about a repository |
| `github_list_issues` | List issues in a repository |
| `github_get_issue` | Get details of a specific issue |
| `github_create_issue` | Create a new issue |
| `github_list_pull_requests` | List pull requests in a repository |
| `github_get_pull_request` | Get details of a specific pull request |
| `github_get_file_contents` | Get file or directory contents from a repo |
| `github_list_branches` | List branches in a repository |
| `github_list_commits` | List commits in a repository |
| `github_search_code` | Search for code across GitHub |

### Jira (8 tools)

| Tool | Description |
|---|---|
| `jira_list_projects` | List all accessible Jira projects |
| `jira_search_issues` | Search issues using JQL |
| `jira_get_issue` | Get full details of an issue |
| `jira_create_issue` | Create a new issue |
| `jira_update_issue` | Update fields of an existing issue |
| `jira_add_comment` | Add a comment to an issue |
| `jira_list_transitions` | List available workflow transitions |
| `jira_transition_issue` | Transition an issue to a new status |

### REST API (5 tools)

| Tool | Description |
|---|---|
| `rest_get` | Make an HTTP GET request |
| `rest_post` | Make an HTTP POST request |
| `rest_put` | Make an HTTP PUT request |
| `rest_patch` | Make an HTTP PATCH request |
| `rest_delete` | Make an HTTP DELETE request |

### Oracle Database (5 tools)

| Tool | Description |
|---|---|
| `oracle_execute_query` | Execute a SELECT query and return results as JSON |
| `oracle_execute_statement` | Execute an INSERT, UPDATE, or DELETE statement |
| `oracle_list_tables` | List tables in the database |
| `oracle_describe_table` | Describe columns of a table |
| `oracle_call_procedure` | Call a stored procedure |

### MongoDB (9 tools)

| Tool | Description |
|---|---|
| `mongo_list_collections` | List all collections in the database |
| `mongo_find` | Find documents with a filter |
| `mongo_find_one` | Find a single document |
| `mongo_insert_document` | Insert one document |
| `mongo_insert_many` | Insert multiple documents |
| `mongo_update_document` | Update a document |
| `mongo_delete_document` | Delete a document |
| `mongo_count` | Count documents matching a filter |
| `mongo_aggregate` | Run an aggregation pipeline |

## Adding a New Integration

1. Create `mcp_server/tools/<name>/` with `client.py` and `tools.py`
2. Decorate each tool function with `@tool("Category Name")` from `mcp_server.registry`
3. Add the module import to `mcp_server/tools/__init__.py`

The tool will automatically appear in the browser UI and be available to MCP clients.
