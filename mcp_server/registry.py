"""Shared tool registry — tracks all registered tools with metadata."""
import inspect
from typing import Any, Callable

_registry: dict[str, dict] = {}  # name -> {fn, category}

_TEXTAREA_PARAMS = {
    "body", "content", "query", "pipeline", "statement", "sql",
    "payload", "data", "filter", "update", "aggregation",
}


def tool(category: str) -> Callable:
    """Decorator: registers a function with FastMCP and the local registry."""
    from mcp_server.server import mcp

    def decorator(fn: Callable) -> Callable:
        mcp.tool()(fn)
        _registry[fn.__name__] = {"fn": fn, "category": category}
        return fn

    return decorator


def call(name: str, params: dict) -> Any:
    entry = _registry.get(name)
    if not entry:
        raise ValueError(f"Unknown tool: {name}")
    return entry["fn"](**params)


def get_metadata() -> list[dict]:
    result = []
    for name, entry in _registry.items():
        fn = entry["fn"]
        sig = inspect.signature(fn)
        doc = (fn.__doc__ or "").strip()
        desc = doc.split("\n")[0] if doc else ""

        params = []
        for pname, param in sig.parameters.items():
            ann = param.annotation
            if ann is int:
                ptype = "int"
            elif ann is float:
                ptype = "float"
            elif ann is bool:
                ptype = "bool"
            else:
                ptype = "str"

            if pname in _TEXTAREA_PARAMS:
                ptype = "text"

            params.append({
                "name": pname,
                "type": ptype,
                "required": param.default is inspect.Parameter.empty,
                "default": None if param.default is inspect.Parameter.empty else param.default,
            })

        result.append({
            "name": name,
            "description": desc,
            "category": entry["category"],
            "params": params,
        })
    return result
