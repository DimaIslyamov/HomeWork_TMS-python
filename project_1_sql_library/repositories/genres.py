"""Genres repository module."""

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.book_model import BookModel
from models.genre_model import GenreModel
from repositories.interfaces import IGenreRepository


class GenreRepository(IGenreRepository):
    """CRUD methods for Genre repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: GenreModel) -> int:
        """Add Genre to database."""
        self._session.add(entity)

        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise

        return entity.id

    def get_by_id(self, entity_id: int) -> GenreModel | None:
        """Get Genre by id."""
        return self._session.get(GenreModel, entity_id)

    def get_all(self) -> list[GenreModel]:
        """Get all Genres."""
        statement = (select(GenreModel).order_by(GenreModel.name))

        return list(self._session.scalars(statement).all())

    def update(self, entity: GenreModel) -> bool:
        """Update Genre in database."""
        if entity.id is None:
            return False

        genre_model = self._session.get(GenreModel, entity.id)

        if genre_model is None:
            return False

        genre_model.name = entity.name

        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
            raise

        return True

    def delete(self, entity_id: int) -> bool:
        """Delete Genre in database."""
        genre_model = self._session.get(GenreModel, entity_id)
        if genre_model is not None:
            self._session.delete(genre_model)

            try:
                self._session.commit()
            except IntegrityError:
                self._session.rollback()
                raise

            return True

        return False

    def get_by_name(self, name: str) -> list[GenreModel]:
        """Get Genres by name."""
        statement = (select(GenreModel)
                     .where(GenreModel.name == name)
                     .order_by(GenreModel.id))

        return list(self._session.scalars(statement).all())

    def search_by_name(self, pattern: str) -> list[GenreModel]:
        """Search Genres by name."""
        statement = ((select(GenreModel)
                     .where(GenreModel.name.ilike(f"%{pattern}%")))
                     .order_by(GenreModel.id))

        return list(self._session.scalars(statement).all())

    def get_books(self, genre_id: int) -> list[BookModel]:
        """Get Books by genre_id."""
        statement = (select(BookModel)
                     .join(BookModel.genres)
                     .where(GenreModel.id == genre_id)
                     .order_by(BookModel.id))

        return list(self._session.scalars(statement).all())
