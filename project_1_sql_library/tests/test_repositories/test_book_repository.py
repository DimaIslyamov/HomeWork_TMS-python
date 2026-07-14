"""Tests for book repository."""
from models import BookModel
from repositories.books import BookRepository

from tests.conftest import book_repository


def test_add_and_get_by_id(
    book_repository: BookRepository,
) -> None:
    """Test adding and getting book by id."""

    book_model = BookModel(
        title="The Witcher",
        year=1999,
        description="The Fantasy about geralt from rivia",
    )

    book_id = book_repository.add(book_model)
    saved_genre = book_repository.get_by_id(book_id)

    assert book_id > 0
    assert saved_genre is not None
    assert saved_genre.id == book_id
    assert saved_genre.title == "The Witcher"
    assert saved_genre.year == 1999
    assert saved_genre.description == "The Fantasy about geralt from rivia"


def test_get_by_id_returns_none_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return None when book does not exist."""

    book = book_repository.get_by_id(999)

    assert book is None


def test_get_all_returns_books_ordered_by_id(
    book_repository: BookRepository,
) -> None:
    """Repository should return all books ordered by id."""

    first_book = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    second_book = book_repository.add(
        BookModel(
            title="Clean code",
            year=2019,
            description="A book about clean code",
        )
    )

    books = book_repository.get_all()

    assert len(books) == 2
    assert [book.id for book in books] == [first_book, second_book]


def test_update_existing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should update existing book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    updated_book = BookModel(
        id=book_id,
        title="Clean code",
        year=2019,
        description="A book about clean code",
    )

    result = book_repository.update(updated_book)
    saved_book = book_repository.get_by_id(book_id)

    assert result is True
    assert saved_book is not None
    assert saved_book.title == "Clean Code"
    assert saved_book.year == 2019
    assert saved_book.id == book_id


def test_update_returns_false_when_book_has_no_id(
    book_repository: BookRepository,
) -> None:
    """Repository should return None when book does not exist."""

    pass


def test_update_returns_false_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return None when book does not exist."""

    pass