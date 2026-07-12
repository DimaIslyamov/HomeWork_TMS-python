from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from models import AuthorModel, BookModel, GenreModel

T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    """Base interface for repositories with CRUD operations"""

    @abstractmethod
    def add(self, entity: T) -> int:
        """Add an entity and return its id """

    @abstractmethod
    def get_by_id(self, entity_id: int) -> T | None:
        """Get entity by id"""

    @abstractmethod
    def get_all(self) -> list[T]:
        """Get all entities"""

    @abstractmethod
    def update(self, entity: T) -> bool:
        """Update entity"""

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete entity"""


class ISearchRepository(ABC, Generic[T]):
    """Search repository interface."""

    @abstractmethod
    def search_by_name(self, pattern: str) -> list[T]:
        """Search entity by name"""


class IAuthorRepository(IRepository[AuthorModel],
                        ISearchRepository[AuthorModel],
                        ABC):
    """Interface repository for authors"""

    @abstractmethod
    def get_by_name(self, name: str) -> list[AuthorModel]:
        """Get author by name"""

    @abstractmethod
    def get_books(self, author_id: int) -> list[BookModel]:
        """Get author books by author_id"""


class IGenreRepository(IRepository[GenreModel],
                       ISearchRepository[GenreModel],
                       ABC):
    """Interface repository for genres"""

    @abstractmethod
    def get_by_name(self, name: str) -> list[GenreModel]:
        """Get genre by name"""

    @abstractmethod
    def get_books(self, genre_id: int) -> list[BookModel]:
        """Get genre books by genre_id"""


class IBookRepository(IRepository[BookModel],
                      ISearchRepository[BookModel],
                      ABC):
    """Interface repository for books"""

    @abstractmethod
    def add_author(self, book_id: int, author_id: int) -> bool:
        """Add author to book"""

    @abstractmethod
    def add_genre(self, book_id: int, genre_id: int) -> bool:
        """Add genre to book"""

    @abstractmethod
    def get_authors(self, book_id: int) -> list[AuthorModel]:
        """Get authors of book by book_id."""

    @abstractmethod
    def get_genres(self, book_id: int) -> list[GenreModel]:
        """Get genre of books by book_id"""

    @abstractmethod
    def search_by_author(self, author_name: str) -> list[BookModel]:
        """Search books by author name."""

    @abstractmethod
    def search_by_genre(self, genre_name: str) -> list[BookModel]:
        """Search genre by genre name."""
