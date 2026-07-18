"""Shared pytest fixtures for BookFlow tests."""

from collections.abc import Generator
from pathlib import Path

from sqlite3 import Connection as SQLite3Connection, Cursor
from typing import Any

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from database.base import Base
import models  # noqa: F401

from repositories.authors import AuthorRepository
from repositories.books import BookRepository
from repositories.genres import GenreRepository


TEST_DATABASE_PATH = Path(__file__).parent / "test.db"
TEST_DATABASE_URL = f"sqlite:///{TEST_DATABASE_PATH.as_posix()}"


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine, None, None]:
    """Create an isolated SQLite engine for the test session."""

    engine = create_engine(TEST_DATABASE_URL, echo=False)

    @event.listens_for(engine, "connect")
    def enable_test_sqlite_foreign_keys(
        dbapi_connection: Any,
        _: Any,
    ) -> None:
        """Enable foreign key constraints for the test SQLite database."""

        if isinstance(dbapi_connection, SQLite3Connection):
            cursor: Cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    Base.metadata.create_all(engine)

    yield engine

    Base.metadata.drop_all(engine)
    engine.dispose()

    if TEST_DATABASE_PATH.exists():
        TEST_DATABASE_PATH.unlink()


@pytest.fixture
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    """Provide a clean database session for each test."""

    session_factory = sessionmaker(
        bind=test_engine,
        class_=Session,
        autoflush=True,
        expire_on_commit=False,
    )

    session = session_factory()

    yield session

    session.rollback()
    session.close()

    for table in reversed(Base.metadata.sorted_tables):
        with test_engine.begin() as connection:
            connection.execute(table.delete())


@pytest.fixture
def author_repository(db_session: Session) -> AuthorRepository:
    """Provide an author repository for tests."""
    return AuthorRepository(db_session)


@pytest.fixture
def book_repository(db_session: Session) -> BookRepository:
    """Provide a book repository for tests."""
    return BookRepository(db_session)


@pytest.fixture
def genre_repository(db_session: Session) -> GenreRepository:
    """Provide a genre repository for tests."""
    return GenreRepository(db_session)
