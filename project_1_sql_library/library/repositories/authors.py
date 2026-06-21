"""Authors repository module"""

from sqlite3 import Row

from library.database.connection import Database
from library.models.entities import Author, Book
from library.repositories.base import (
    format_date,
    parse_date,
    require_lastrowid,
    matches_partial
)

from library.repositories.interfaces import IAuthorRepository, T


class AuthorRepository(IAuthorRepository):
    """CRUD methods for Authors"""

    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def _row_to_author(row: Row) -> Author:
        return Author(
            id=row['id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            birth_date=parse_date(row['birth_date']),
        )


    def add(self, entity: Author) -> int:
        """Add an author to the database"""
        cursor = self.db.execute(
            'INSERT INTO authors VALUES (?, ?, ?, ?)',
            (
                entity.id,
                entity.first_name,
                entity.last_name,
                entity.birth_date
            )
        )
        return require_lastrowid(cursor)

    def get_all(self) -> list[Author]:
        """Get all authors"""
        rows = self.db.fetchall(
            """
            SELECT * 
            FROM authors
            """
        )
        return [self._row_to_author(row) for row in rows]

    def get_by_id(self, entity_id: int) -> Author | None:
        """Get an author by its id"""
        row = self.db.fetchone(
            """
            SELECT * FROM authors 
            WHERE id = ?
            """,
            (entity_id,)
        )

        if row is None:
            return None

        return self._row_to_author(row)

    def update(self, entity: Author) -> bool:
        """Update an author"""
        if entity.id is None:
            return False

        cursor = self.db.execute(
            """
            UPDATE authors 
            SET first_name = ?,
                last_name = ?, 
                birth_date = ?
            WHERE id = ?,
            """,
            (
                entity.first_name,
                entity.last_name,
                entity.birth_date,
                entity.id
            )
        )

        return cursor.rowcount > 0

    def delete(self, entity_id: int) -> bool:
        """Delete an author"""
        cursor = self.db.execute(
            'DELETE FROM authors WHERE id = ?',
            (entity_id,))

        return cursor.rowcount > 0

    def get_by_name(self, name: str) -> list[Author]:
        """Get an authors by its name"""
        rows = self.db.fetchall(
            'SELECT * FROM authors WHERE first_name = ? OR last_name = ?',
            (name, name)
        )

        return [self._row_to_author(row) for row in rows]

    def search_by_name(self, pattern: str) -> list[Author]:
        """Search authors by a pattern"""
        authors = self.get_all()

        return [author for author in
                authors if matches_partial(
                f"{author.first_name} {author.last_name}",
                pattern
            )]

    def get_books(self, author_id: int) -> list[Book]:
        """Get books by an author"""
        rows = self.db.fetchall(
            """
            SELECT books.* FROM books 
            
            JOIN books_authors 
            ON books.id = books_authors.book_id
            
            WHERE books_authors.author_id = ?
            """,
            (author_id,)
        )

        return [Book(
            id=row["id"],
            title=row["title"],
            year=row["year"],
            description=row["description"],
        )
        for row in rows
        ]