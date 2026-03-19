# GitHub MCP Server

A Python-based [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes GitHub tools for use by AI assistants.

## Prerequisites

- Python 3.10+
- A [GitHub Personal Access Token](https://github.com/settings/tokens)

## Installation

```bash
pip install -e .
```

## Configuration

Set your GitHub token as an environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

On Windows (PowerShell):

```powershell
$env:GITHUB_TOKEN = "ghp_your_token_here"
```

## Usage

### Run directly

```bash
github-mcp-server
```

### VS Code / Copilot

Add to your `.vscode/mcp.json`:

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "github_mcp_server"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
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
    "github": {
      "command": "python",
      "args": ["-m", "github_mcp_server"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

## Available Tools

| Tool | Description |
|---|---|
| `search_repositories` | Search for GitHub repositories |
| `get_repository` | Get detailed info about a repository |
| `list_issues` | List issues in a repository |
| `get_issue` | Get details of a specific issue |
| `create_issue` | Create a new issue |
| `list_pull_requests` | List pull requests in a repository |
| `get_pull_request` | Get details of a specific pull request |
| `get_file_contents` | Get file or directory contents from a repo |
| `search_code` | Search for code across GitHub |
| `list_branches` | List branches in a repository |
| `create_or_update_file` | Create or update a file in a repository |
| `list_commits` | List commits in a repository |