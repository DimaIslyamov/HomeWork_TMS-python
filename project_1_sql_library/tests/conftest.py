"""Shared pytest fixtures for BookFlow tests."""

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import create_engine
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

    # Создаются тестовый engine, файл tests/test.db и таблицы.
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    Base.metadata.create_all(engine)

    yield engine

    # Удаляются таблицы, закрывается engine и удаляется тестовая база.
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
    """Provide an author repository for the test session."""
    return AuthorRepository(db_session)


@pytest.fixture
def book_repository(db_session: Session) -> BookRepository:
    """Provide an author repository for the test session."""
    return BookRepository(db_session)


@pytest.fixture
def genre_repository(db_session: Session) -> GenreRepository:
    """Provide an author repository for the test session."""
    return GenreRepository(db_session)
