import json
import os
import httpx
from mcp_server.registry import tool


def _client() -> httpx.Client:
    base_url = os.environ.get("REST_API_BASE_URL", "")
    headers: dict = {"Content-Type": "application/json", "Accept": "application/json"}
    token = os.environ.get("REST_API_TOKEN")
    token_header = os.environ.get("REST_API_TOKEN_HEADER", "Authorization")
    token_prefix = os.environ.get("REST_API_TOKEN_PREFIX", "Bearer")
    if token:
        headers[token_header] = f"{token_prefix} {token}" if token_prefix else token
    return httpx.Client(base_url=base_url, headers=headers, timeout=30)


def _response(resp: httpx.Response) -> str:
    try:
        return json.dumps(resp.json(), indent=2)
    except Exception:
        return resp.text


@tool("REST API")
def rest_get(path: str, params: str = "") -> str:
    """Make an HTTP GET request. params as key=value&key2=value2."""
    with _client() as client:
        query = dict(p.split("=", 1) for p in params.split("&") if "=" in p) if params else {}
        resp = client.get(path, params=query)
        return _response(resp)


@tool("REST API")
def rest_post(path: str, payload: str = "") -> str:
    """Make an HTTP POST request. payload as JSON string."""
    with _client() as client:
        body = json.loads(payload) if payload.strip() else {}
        resp = client.post(path, json=body)
        return _response(resp)


@tool("REST API")
def rest_put(path: str, payload: str = "") -> str:
    """Make an HTTP PUT request. payload as JSON string."""
    with _client() as client:
        body = json.loads(payload) if payload.strip() else {}
        resp = client.put(path, json=body)
        return _response(resp)


@tool("REST API")
def rest_patch(path: str, payload: str = "") -> str:
    """Make an HTTP PATCH request. payload as JSON string."""
    with _client() as client:
        body = json.loads(payload) if payload.strip() else {}
        resp = client.patch(path, json=body)
        return _response(resp)


@tool("REST API")
def rest_delete(path: str) -> str:
    """Make an HTTP DELETE request."""
    with _client() as client:
        resp = client.delete(path)
        return _response(resp)
