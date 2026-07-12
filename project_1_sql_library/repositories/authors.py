"""Authors repository module"""

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from models.author_model import AuthorModel
from models.book_model import BookModel
from repositories.interfaces import IAuthorRepository


class AuthorRepository(IAuthorRepository):
    """CRUD methods for Authors"""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: AuthorModel) -> int:
        """Add an author to the database"""
        self._session.add(entity)
        self._session.commit()

        return entity.id

    def get_by_id(self, entity_id: int) -> AuthorModel | None:
        """Get an author by its id"""
        return self._session.get(AuthorModel, entity_id)

    def get_all(self) -> list[AuthorModel]:
        """Get all authors"""
        statement = select(AuthorModel).order_by(AuthorModel.id)

        return list(self._session.scalars(statement).all())

    def update(self, entity: AuthorModel) -> bool:
        """Update an author"""
        if entity.id is None:
            return False

        update_author_model = self._session.get(AuthorModel, entity.id)

        if update_author_model is None:
            return False

        update_author_model.first_name = entity.first_name
        update_author_model.last_name = entity.last_name
        update_author_model.birth_date = entity.birth_date

        self._session.add(update_author_model)
        self._session.commit()

        return True

    def delete(self, entity_id: int) -> bool:
        """Delete an author"""
        delete_author_model = self._session.get(AuthorModel, entity_id)

        if delete_author_model is not None:
            self._session.delete(delete_author_model)
            self._session.commit()

            return True

        return False

    def get_by_name(self, name: str) -> list[AuthorModel]:
        """Get an authors by its name"""
        statement = (
            select(AuthorModel)
            .where(
                or_(
                    AuthorModel.first_name == name,
                    AuthorModel.last_name == name,
                )
            )
            .order_by(AuthorModel.id)
        )
        return list(self._session.scalars(statement).all())

    def search_by_name(self, pattern: str) -> list[AuthorModel]:
        """Search authors by a pattern"""
        statement = (
            select(AuthorModel)
            .where(
                or_(
                    AuthorModel.first_name.ilike(f"%{pattern}%"),
                    AuthorModel.last_name.ilike(f"%{pattern}%"),
                )
            )
            .order_by(AuthorModel.id)
        )
        return list(self._session.scalars(statement).all())

    def get_books(self, author_id: int) -> list[BookModel]:
        """Get Books by genre_id."""
        statement = (select(BookModel)
                     .join(BookModel.authors)
                     .where(AuthorModel.id == author_id)
                     .order_by(BookModel.id))

        return list(self._session.scalars(statement).all())
