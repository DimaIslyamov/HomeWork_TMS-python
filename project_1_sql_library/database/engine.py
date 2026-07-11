"""SQLAlchemy engine configuration."""

from sqlite3 import Connection as SQLiteConnection, Cursor
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

from database.connection import DEFAULT_DATABASE_PATH


DATABASE_URL = f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, echo=False)


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection: Any, _: Any) -> None:
    """Enable foreign key constraint for SQLite connection."""

    if isinstance(dbapi_connection, SQLiteConnection):
        cursor: Cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
