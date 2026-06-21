"""Books repository module."""

from sqlite3 import Row

from library.database.connection import Database
from library.models.entities import Book, Author, Genre
from library.repositories.base import (
    require_lastrowid,
    matches_partial,
    parse_date,
)

from library.repositories.interfaces import IBookRepository


class BookRepository(IBookRepository):
    """CRUD methods for Book repository."""

    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def _row_to_book(row: Row) -> Book:
        """Convert row to Book."""
        return Book(
            id=row['id'],
            title=row['title'],
            year=row['year'],
            description=row['description'],
        )

    @staticmethod
    def _row_to_author(row: Row) -> Author:
        """Convert row to Author."""
        return Author(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            birth_date=parse_date(row['birth_date']),
        )

    @staticmethod
    def _row_to_genre(row: Row) -> Genre:
        """Convert row to Genre."""
        return Genre(
            id=row['id'],
            name=row['name'],
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

        return [
            book for book in books
            if matches_partial(book.title, pattern=pattern)
        ]

    def add_author(self, book_id: int, author_id: int) -> None:
        """Add an author to a book."""
        self.db.execute(
            """
            INSERT OR IGNORE INTO books_authors (book_id, author_id)
            VALUES (?, ?)
            """,
            (book_id, author_id)
        )

    def add_genre(self, book_id: int, genre_id: int) -> None:
        """Add a genre to a book."""
        self.db.execute(
            """
            INSERT OR IGNORE INTO books_genres (book_id, genre_id)
            VALUES (?, ?)
            """,
            (book_id, genre_id)
        )

    def get_authors(self, book_id: int) -> list[Author]:
        """Get all authors of a book."""
        rows = self.db.fetchall(
            """
            SELECT authors.*
            FROM authors
            JOIN books_authors
                ON authors.id = books_authors.author_id
            WHERE books_authors.book_id = ?
            """,
            (book_id,)
        )
        return [self._row_to_author(row) for row in rows]

    def get_genres(self, book_id: int) -> list[Genre]:
        """Get all genres of a book."""
        rows = self.db.fetchall(
            """
            SELECT genres.*
            FROM genres
            JOIN books_genres
                ON genres.id = books_genres.genre_id
            WHERE books_genres.book_id = ?
            """,
            (book_id,)
        )
        return [self._row_to_genre(row) for row in rows]

    def search_by_author(self, author_name: str) -> list[Book]:
        """Search books by author name."""
        rows = self.db.fetchall(
            """
            SELECT DISTINCT books.*
            FROM books
            JOIN books_authors
                ON books.id = books_authors.book_id
            JOIN authors
                ON authors.id = books_authors.author_id
            WHERE authors.first_name LIKE ?
               OR authors.last_name LIKE ?
               OR authors.first_name || ' ' || authors.last_name LIKE ?
            """,
            (
                f"%{author_name}%",
                f"%{author_name}%",
                f"%{author_name}%",
            )
        )
        return [self._row_to_book(row) for row in rows]

    def search_by_genre(self, genre_name: str) -> list[Book]:
        """Search books by genre name."""
        rows = self.db.fetchall(
            """
            SELECT DISTINCT books.*
            FROM books
            JOIN books_genres
                ON books.id = books_genres.book_id
            JOIN genres
                ON genres.id = books_genres.genre_id
            WHERE genres.name LIKE ?
            """,
            (f"%{genre_name}%",)
        )
        return [self._row_to_book(row) for row in rows]
