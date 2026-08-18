# import libs
from pathlib import Path
import sqlite3


DATABASE_NAME = "nasa9_all_phases.sqlite"


def get_database_path() -> Path:
    """
    Return the path to the embedded NASA-9 SQLite database.
    """
    return Path(__file__).with_name(DATABASE_NAME)


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite connection.

    Returns
    -------
    sqlite3.Connection
        SQLite connection configured to return rows
        as sqlite3.Row objects.
    """
    db_path = get_database_path()

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    return connection
