"""Books repository module."""

from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session

from models.author_model import AuthorModel
from models.genre_model import GenreModel
from models.book_model import BookModel
from repositories.interfaces import IBookRepository


class BookRepository(IBookRepository):
    """CRUD methods for Book repository."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, entity: BookModel) -> int:
        """Add a book to the database"""
        self._session.add(entity)
        self._session.commit()

        return entity.id

    def get_by_id(self, entity_id: int) -> BookModel | None:
        """Get a book by its id"""
        return self._session.get(BookModel, entity_id)

    def get_all(self) -> list[BookModel]:
        """Get all books"""
        statement = select(BookModel).order_by(BookModel.id)

        return list(self._session.scalars(statement).all())

    def update(self, entity: BookModel) -> bool:
        """Update a book model"""
        if entity.id is None:
            return False

        update_book_model = self._session.get(BookModel, entity.id)

        if update_book_model is None:
            return False

        update_book_model.title = entity.title
        update_book_model.year = entity.year
        update_book_model.description = entity.description

        self._session.add(update_book_model)
        self._session.commit()

        return True

    def delete(self, entity_id: int) -> bool:
        """Delete a book"""
        delete_book_model = self._session.get(BookModel, entity_id)

        if delete_book_model is not None:
            self._session.delete(delete_book_model)
            self._session.commit()

            return True

        return False

    def search_by_name(self, pattern: str) -> list[BookModel]:
        """Search books by name"""
        statement = (
            select(BookModel)
            .where(BookModel.title.ilike(f"%{pattern}%"))
            .order_by(BookModel.id))

        return list(self._session.scalars(statement).all())

    def add_author(self, book_id: int, author_id: int) -> bool:
        """Add an author to a book."""
        book = self._session.get(BookModel, book_id)
        author = self._session.get(AuthorModel, author_id)

        if book is None or author is None:
            return False

        if author in book.authors:
            return False

        book.authors.append(author)
        self._session.commit()

        return True


    def add_genre(self, book_id: int, genre_id: int) -> bool:
        """Add a genre to a book."""
        book = self._session.get(BookModel, book_id)
        genre = self._session.get(GenreModel, genre_id)

        if book is None or genre is None:
            return False

        if genre in book.genres:
            return False

        book.genres.add(genre)
        self._session.commit()

        return True

    def get_authors(self, book_id: int) -> list[AuthorModel]:
        """Get all authors of a book."""
        statement = (
            select(AuthorModel)
            .join(AuthorModel)
            .where(BookModel.id == book_id)
            .order_by(AuthorModel.id)
        )
        return list(self._session.scalars(statement).unique().all())

    def get_genres(self, book_id: int) -> list[GenreModel]:
        """Get all genres of a book."""
        statement = (
            select(GenreModel)
            .join(GenreModel)
            .where(BookModel.id == book_id)
            .order_by(GenreModel.id)
        )
        return list(self._session.scalars(statement).unique().all())

    def search_by_author(self, author_name: str) -> list[BookModel]:
        """Search books by author name."""
        statement = (
            select(BookModel)
            .join(BookModel.authors)
            .where(
                or_(
                    AuthorModel.first_name.ilike(f"%{author_name}%"),
                    AuthorModel.last_name.ilike(f"%{author_name}%"),
                )
            )
            .order_by(BookModel.id)
        )
        return list(self._session.scalars(statement).unique().all())

    def search_by_genre(self, genre_name: str) -> list[BookModel]:
        """Search books by genre name."""
        statement = (
            select(BookModel)
            .join(BookModel.genres)
            .where(GenreModel.name.ilike(f"%{genre_name}%"))
            .order_by(BookModel.id)
        )
        return list(self._session.scalars(statement).unique().all())
