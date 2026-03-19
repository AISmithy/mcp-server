"""Auto-loads all tool integrations. Each integration loads only if its package is importable."""
import logging

logger = logging.getLogger(__name__)

_INTEGRATIONS = [
    ("mcp_server.tools.github.tools", "GitHub"),
    ("mcp_server.tools.jira.tools", "Jira"),
    ("mcp_server.tools.rest_api.tools", "REST API"),
    ("mcp_server.tools.oracle.tools", "Oracle"),
    ("mcp_server.tools.mongodb.tools", "MongoDB"),
]


def load_all() -> None:
    import importlib
    for module_path, name in _INTEGRATIONS:
        try:
            importlib.import_module(module_path)
            logger.info("%s tools loaded", name)
        except ImportError as e:
            logger.warning("%s tools not available (missing dependency): %s", name, e)
        except Exception as e:
            logger.warning("%s tools failed to load: %s", name, e)
