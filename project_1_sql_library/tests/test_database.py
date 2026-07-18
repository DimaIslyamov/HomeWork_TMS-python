"""Tests for the isolated test database."""

from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from models.author_model import AuthorModel


def test_database_session_can_save_author(db_session: Session) -> None:
    """Test that the isolated database session can persist a model."""

    author = AuthorModel(
        first_name="Robert",
        last_name="Martin",
        birth_date=None,
    )

    db_session.add(author)
    db_session.commit()

    saved_author = db_session.scalar(
        select(AuthorModel).where(
            AuthorModel.first_name == "Robert",
        )
    )

    assert saved_author is not None
    assert saved_author.id is not None
    assert saved_author.first_name == "Robert"
    assert saved_author.last_name == "Martin"


def test_foreign_keys_are_enabled(
    test_engine: Engine,
) -> None:
    """Test database should enforce SQLite foreign keys."""

    with test_engine.connect() as connection:
        foreign_keys_enabled = connection.scalar(
            text("PRAGMA foreign_keys")
        )

    assert foreign_keys_enabled == 1
