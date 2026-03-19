import json
from mcp_server.registry import tool
from mcp_server.tools.oracle.client import get_connection


def _serialize(row: tuple, columns: list[str]) -> dict:
    result = {}
    for col, val in zip(columns, row):
        if hasattr(val, "isoformat"):
            result[col] = val.isoformat()
        elif hasattr(val, "read"):
            result[col] = val.read()
        else:
            result[col] = val
    return result


@tool("Oracle")
def oracle_execute_query(sql: str, max_rows: int = 100) -> str:
    """Execute a SELECT query and return results as JSON."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = []
        for i, row in enumerate(cursor):
            if i >= max_rows:
                break
            rows.append(_serialize(row, columns))
        return json.dumps({"columns": columns, "rows": rows, "count": len(rows)}, indent=2)


@tool("Oracle")
def oracle_execute_statement(sql: str) -> str:
    """Execute an INSERT, UPDATE, or DELETE statement."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return json.dumps({"rowcount": cursor.rowcount, "executed": True}, indent=2)


@tool("Oracle")
def oracle_list_tables(schema: str = "") -> str:
    """List tables in the Oracle database (optionally filter by schema)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if schema:
            cursor.execute(
                "SELECT owner, table_name FROM all_tables WHERE UPPER(owner) = UPPER(:1) ORDER BY table_name",
                [schema],
            )
        else:
            cursor.execute("SELECT owner, table_name FROM user_tables ORDER BY table_name")
        rows = [{"owner": r[0], "table_name": r[1]} for r in cursor]
        return json.dumps(rows, indent=2)


@tool("Oracle")
def oracle_describe_table(table_name: str, schema: str = "") -> str:
    """Describe the columns of an Oracle table."""
    with get_connection() as conn:
        cursor = conn.cursor()
        owner_filter = "UPPER(owner) = UPPER(:2) AND" if schema else ""
        params = [table_name.upper(), schema] if schema else [table_name.upper()]
        cursor.execute(
            f"SELECT column_name, data_type, data_length, nullable "
            f"FROM all_columns WHERE {owner_filter} UPPER(table_name) = UPPER(:1) "
            f"ORDER BY column_id",
            params,
        )
        columns = [
            {"column_name": r[0], "data_type": r[1], "data_length": r[2], "nullable": r[3]}
            for r in cursor
        ]
        return json.dumps(columns, indent=2)


@tool("Oracle")
def oracle_call_procedure(procedure_name: str, params: str = "") -> str:
    """Call a stored procedure. params as comma-separated values."""
    with get_connection() as conn:
        cursor = conn.cursor()
        args = [p.strip() for p in params.split(",") if p.strip()] if params else []
        cursor.callproc(procedure_name, args)
        conn.commit()
        return json.dumps({"procedure": procedure_name, "executed": True}, indent=2)
