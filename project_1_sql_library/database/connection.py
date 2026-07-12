import sqlite3

from typing import Any, cast
from pathlib import Path

DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / 'data' / "library.db"


class Database:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = db_path or DEFAULT_DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection: sqlite3.Connection | None = None

    def connect(self) -> sqlite3.Connection:
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path)
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def execute(self,
                query: str,
                params: tuple[Any, ...] = (),
                ) -> sqlite3.Cursor:
        """Execute an SQL query"""

        connection = self.connect()
        cursor = connection.execute(query, params)
        connection.commit()

        return cursor

    def fetchone(self,
                 query: str,
                 params: tuple[Any, ...] = (),
                 ) -> sqlite3.Row | None:
        """Return one row from the query"""

        row = self.connect().execute(query, params).fetchone()

        return cast(sqlite3.Row | None, row)

    def fetchall(self, query: str,
                 params: tuple[Any, ...] = ()
                 ) -> list[sqlite3.Row]:
        """Return all rows from a SQL query"""

        return self.connect().execute(query, params).fetchall()

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self,
                 exc_type: Any,
                 exc_val: Any,
                 exc_tb: Any,) -> None:
        if self._connection is not None:
            if exc_type is None:
                self._connection.commit()
            self.close()
