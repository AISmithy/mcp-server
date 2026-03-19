import sys
from mcp_server.tools import load_all
from mcp_server.server import mcp


def main() -> None:
    load_all()
    transport = "sse" if "--sse" in sys.argv else "stdio"
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
