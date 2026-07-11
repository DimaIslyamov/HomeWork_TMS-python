"""Genres repository module."""

from sqlite3 import Row

from database.connection import Database
from models.entities import Genre, Book
from repositories.base import require_lastrowid, matches_partial

from repositories.interfaces import IGenreRepository


class GenreRepository(IGenreRepository):
    """CRUD methods for Genre repository."""

    def __init__(self, db: Database):
        self.db = db

    @staticmethod
    def _row_to_genre(row: Row) -> Genre:
        """Convert row to Genre"""
        return Genre(
            id=row['id'],
            name=row['name'],
        )

    def add(self, entity: Genre) -> int:
        """Add Genre to database."""
        cursor = self.db.execute(
            """
            INSERT INTO genres (id, name) 
            VALUES (?, ?)
            """,
            (entity.id, entity.name)
        )
        return require_lastrowid(cursor)

    def get_by_id(self, entity_id: int) -> Genre | None:
        """Get Genre by id."""
        row = self.db.fetchone(
            'SELECT * FROM genres WHERE id = ?',
            (entity_id,)
        )

        if row is None:
            return None

        return self._row_to_genre(row)

    def get_all(self) -> list[Genre]:
        """Get all Genres."""
        rows = self.db.fetchall(
            'SELECT * FROM genres'
        )
        return [self._row_to_genre(row) for row in rows]

    def update(self, entity: Genre) -> bool:
        """Update Genre in database."""
        if entity.id is None:
            return False

        cursor = self.db.execute(
            'UPDATE genres SET name = ? WHERE id = ?',
            (entity.name, entity.id)
        )
        return cursor.rowcount > 0

    def delete(self, entity_id: int) -> bool:
        """Delete Genre in database."""
        cursor = self.db.execute(
            'DELETE FROM genres WHERE id = ?',
            (entity_id,)
        )
        return cursor.rowcount > 0

    def get_by_name(self, name: str) -> list[Genre]:
        """Get Genres by name."""
        rows = self.db.fetchall(
            'SELECT * FROM genres WHERE name = ?',
            (name,)
        )
        return [self._row_to_genre(row) for row in rows]

    def search_by_name(self, pattern: str) -> list[Genre]:
        """Search Genres by name."""
        genres = self.get_all()

        return [
            genre for genre in genres
            if matches_partial(genre.name, pattern)
        ]

    def get_books(self, genre_id: int) -> list[Book]:
        """Get Books by genre_id."""
        rows = self.db.fetchall(
            """
            SELECT books.* FROM books
            JOIN books_genres
            ON books.id = books_genres.book_id
            WHERE books_genres.genre_id = ?
            """,
            (genre_id,)
        )

        return [Book(
            id=row["id"],
            title=row["title"],
            year=row["year"],
            description=row["description"],
        )
            for row in rows
        ]
