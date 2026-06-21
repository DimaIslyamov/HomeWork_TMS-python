"""Books repository module"""

from  sqlite3 import Row

from library.database.connection import Database
from library.models.entities import Book, Author, Genre
from library.repositories.base import (
    require_lastrowid,
    matches_partial
)

from library.repositories.interfaces import IBookRepository, T


class BookRepository(IBookRepository):
    """CRUD methods for Book repository"""

    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def _row_to_book(row: Row) -> Book:
        return Book(
            id=row['id'],
            title=row['title'],
            year=row['year'],
            description=row['description'],
        )


    def add(self, entity: Book) -> int:
        """Add a book to the database"""
        cursor = self.db.execute(
            "INSERT INTO books VALUES (?, ?, ?, ?)",
            (
                entity.id,
                entity.title,
                entity.year,
                entity.description
            )
        )
        return require_lastrowid(cursor)

    def get_by_id(self, entity_id: int) -> Book | None:
        """Get a book by its id"""
        row = self.db.fetchone(
            "SELECT * FROM books WHERE id = ?",
            (entity_id,)
        )

        if row is None:
            return None

        return self._row_to_book(row)

    def get_all(self) -> list[Book]:
        """Get all books"""
        rows = self.db.fetchall(
            "SELECT * FROM books"
        )
        return [self._row_to_book(row) for row in rows]

    def update(self, entity: Book) -> bool:
        """Update a book"""
        if entity.id is None:
            return False

        cursor = self.db.execute(
            """
            UPDATE books
            SET title = ?, year = ?, description = ?
            WHERE id = ?
            """,
            (
                entity.title,
                entity.year,
                entity.description,
                entity.id
            )
        )
        return cursor.rowcount > 0

    def delete(self, entity_id: int) -> bool:
        """Delete a book"""
        cursor = self.db.execute(
            "DELETE FROM books WHERE id = ?",
            (entity_id,)
        )
        return cursor.rowcount > 0

    def search_by_name(self, pattern: str) -> list[Book]:
        """Search books by name"""
        books = self.get_all()

        return [book for book in
                books if matches_partial(
                f"{book.title}",
                pattern=pattern
            )]

    def add_author(self, book_id: int, author_id: int) -> None:
        """Add an author"""
        pass

    def add_genre(self, book_id: int, genre_id: int) -> None:
        """Add a genre"""
        pass

    def get_authors(self, book_id: int) -> list[Author]:
        """Get all authors"""
        pass

    def get_genres(self, book_id: int) -> list[Genre]:
        """Get all genres"""
        pass

    def search_by_author(self, author_name: str) -> list[Book]:
        """Search books by author"""
        pass

    def search_by_genre(self, genre_name: str) -> list[Book]:
        """Search books by genre"""
        pass
