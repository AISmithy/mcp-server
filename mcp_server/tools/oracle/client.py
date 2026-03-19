import os
import oracledb


def get_connection() -> oracledb.Connection:
    user = os.environ.get("ORACLE_USER")
    password = os.environ.get("ORACLE_PASSWORD")
    dsn = os.environ.get("ORACLE_DSN")
    if not all([user, password, dsn]):
        raise RuntimeError(
            "ORACLE_USER, ORACLE_PASSWORD, and ORACLE_DSN environment variables are required."
        )
    return oracledb.connect(user=user, password=password, dsn=dsn)
