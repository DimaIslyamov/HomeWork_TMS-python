"""Tests for book repository."""
from datetime import date

from models import BookModel
from models import AuthorModel
from models import GenreModel

from repositories.authors import AuthorRepository
from repositories.books import BookRepository
from repositories.genres import GenreRepository


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
    saved_book = book_repository.get_by_id(book_id)

    assert book_id > 0
    assert saved_book is not None
    assert saved_book.id == book_id
    assert saved_book.title == "The Witcher"
    assert saved_book.year == 1999
    assert saved_book.description == "The Fantasy about geralt from rivia"


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
    assert saved_book.title == "Clean code"
    assert saved_book.year == 2019
    assert saved_book.id == book_id


def test_update_returns_false_when_book_has_no_id(
    book_repository: BookRepository,
) -> None:
    """Repository should return False when book has no id."""

    book = BookModel(
        title="The Witcher",
        year=1999,
        description="The Fantasy about geralt from rivia",
    )

    result = book_repository.update(book)

    assert result is False


def test_update_returns_false_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return None when book does not exist."""

    book = BookModel(
        id=999,
        title="Unknown",
        year=1999,
        description="The Fantasy about geralt from rivia",
    )

    result = book_repository.update(book)

    assert result is False


def test_delete_existing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should delete existing book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )

    result = book_repository.delete(book_id)

    assert result is True
    assert book_repository.get_by_id(book_id) is None


def test_delete_returns_false_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return None when book does not exist."""

    result = book_repository.delete(999)

    assert result is False


def test_search_by_name_is_partial_and_case_insensitive(
    book_repository: BookRepository,
) -> None:
    """Repository should return all books ordered by name."""

    book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))

    books = book_repository.search_by_name("COD")

    assert len(books) == 2
    assert [item.title for item in books] == ["Clean code", "Python jun code"]


def test_search_by_name_returns_empty_list_when_no_matches(
    book_repository: BookRepository,
) -> None:
    """Repository should return empty list if no matches."""

    book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))

    books = book_repository.search_by_name("Rule")

    assert books == []


# ======== Связь Author ↔ Book =======
def test_add_author_to_book(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should add authors to book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )

    author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Robertson",
            birth_date=date(1999, 1, 1),
        )
    )

    add_author_model = book_repository.add_author(book_id, author_id)
    authors = book_repository.get_authors(book_id)

    assert add_author_model is True
    assert len(authors) == 1
    assert authors[0].first_name == "Robert"
    assert authors[0].last_name == "Robertson"
    assert authors[0].birth_date == date(1999, 1, 1)
    assert authors[0].id == author_id


def test_add_author_returns_false_when_relation_already_exists(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should return false if author already exists."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )

    author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Robertson",
            birth_date=date(1999, 1, 1),
        )
    )

    #  первая связь создается → True
    # повторная связь не создается → False
    # в базе остается один автор

    first_result = book_repository.add_author(book_id, author_id)
    second_result = book_repository.add_author(book_id, author_id)
    authors = book_repository.get_authors(book_id)

    assert first_result is True
    assert second_result is False
    assert len(authors) == 1
    assert authors[0].id == author_id


def test_add_author_returns_false_for_missing_book(
        book_repository: BookRepository,
        author_repository: AuthorRepository,
) -> None:
    """Repository should return false if author doesn't exist."""

    author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Robertson",
            birth_date=date(1999, 1, 1),
        )
    )

    missing_book = book_repository.add_author(999, author_id)

    assert missing_book is False


def test_add_author_returns_false_for_missing_author(
    book_repository: BookRepository,
) -> None:
    """Repository should return false if author doesn't exist."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )

    result = book_repository.add_author(book_id, 999)

    assert result is False


def test_get_authors_returns_authors_assigned_to_book(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should return authors assigned to book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    first_author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Robertson",
            birth_date=date(1999, 1, 1),
        )
    )
    second_author_id = author_repository.add(
        AuthorModel(
            first_name="Igor",
            last_name="Igorson",
            birth_date=date(1999, 1, 1),
        )
    )

    book_repository.add_author(book_id, first_author_id)
    book_repository.add_author(book_id, second_author_id)

    authors = book_repository.get_authors(book_id)

    assert len(authors) == 2
    assert [author.id for author in authors] == [
        first_author_id,
        second_author_id
    ]


def test_get_authors_returns_empty_list_when_book_has_no_authors(
    book_repository: BookRepository,
) -> None:
    """Repository should return an empty list for a book without authors."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="Fantasy novel",
        )
    )

    authors = book_repository.get_authors(book_id)

    assert authors == []


def test_get_authors_returns_empty_list_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return an empty list for a missing book."""

    authors = book_repository.get_authors(999)

    assert authors == []


# ======== Связь Book ↔ Genre =======
def test_add_genre_to_book(
    book_repository: BookRepository,
    genre_repository: GenreRepository,
) -> None:
    """Repository should add a genre to a book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    fantasy_genre_id = genre_repository.add(
        GenreModel(
            name="Fantasy",
        )
    )

    result = book_repository.add_genre(book_id, fantasy_genre_id)
    genres = book_repository.get_genres(book_id)

    assert result is True
    assert len(genres) == 1
    assert genres[0].name == "Fantasy"
    assert genres[0].id == fantasy_genre_id


def test_add_genre_returns_false_when_relation_already_exists(
    book_repository: BookRepository,
    genre_repository: GenreRepository,
) -> None:
    """Repository should return false if genre already exists."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    fantasy_genre_id = genre_repository.add(
        GenreModel(
            name="Fantasy",
        )
    )

    first_result = book_repository.add_genre(book_id, fantasy_genre_id)
    second_result = book_repository.add_genre(book_id, fantasy_genre_id)
    genres = book_repository.get_genres(book_id)

    assert first_result is True
    assert second_result is False
    assert len(genres) == 1
    assert genres[0].id == fantasy_genre_id


def test_add_genre_returns_false_for_missing_book(
        book_repository: BookRepository,
        genre_repository: GenreRepository,
) -> None:
    """Repository should return false if genre doesn't exist."""

    genre_id = genre_repository.add(
        GenreModel(
            name="Fantasy"
        )
    )

    missing_book = book_repository.add_genre(999, genre_id)

    assert missing_book is False


def test_add_genre_returns_false_for_missing_genre(
        genre_repository: GenreRepository,
        book_repository: BookRepository,
) -> None:
    """Repository should return false if genre doesn't exist."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )

    result = book_repository.add_genre(book_id, 999)

    assert result is False


def test_get_genres_returns_genres_assigned_to_book(
        book_repository: BookRepository,
        genre_repository: GenreRepository,
) -> None:
    """Repository should return genres assigned to book."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        )
    )
    first_genre_id = genre_repository.add(GenreModel(name="Fantasy"))
    second_genre_id = genre_repository.add(GenreModel(name="Action"))

    book_repository.add_genre(book_id, first_genre_id)
    book_repository.add_genre(book_id, second_genre_id)

    genres = book_repository.get_genres(book_id)

    assert len(genres) == 2
    assert [genre.id for genre in genres] == [first_genre_id, second_genre_id]


def test_get_genres_returns_empty_list_when_book_has_no_genres(
    book_repository: BookRepository,
) -> None:
    """Repository should return an empty list for a book without genres."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="Fantasy novel",
        )
    )

    genres = book_repository.get_genres(book_id)

    assert genres == []


def test_get_genres_returns_empty_list_for_missing_book(
    book_repository: BookRepository,
) -> None:
    """Repository should return an empty list for a missing book."""

    genres = book_repository.get_genres(999)

    assert genres == []


# ========= Поиск ==========
def test_search_by_author_is_partial_and_case_insensitive(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should find books by partial author name case-insensitively."""

    first_book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    second_book_id = book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    _ = book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))
    author_id = author_repository.add(
        AuthorModel(
            first_name="Dima",
            last_name="Tennesi",
            birth_date=date(1999, 1, 1),
        )
    )

    book_repository.add_author(book_id=first_book_id, author_id=author_id)
    book_repository.add_author(book_id=second_book_id, author_id=author_id)

    result = book_repository.search_by_author("DIM")

    assert len(result) == 2
    assert [item.id for item in result] == [first_book_id, second_book_id]


def test_search_by_author_returns_empty_list_when_no_matches(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should return an empty list when no author matches."""

    first_book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    second_book_id = book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    _ = book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))
    author_id = author_repository.add(
        AuthorModel(
            first_name="Dima",
            last_name="Tennesi",
            birth_date=date(1999, 1, 1),
        )
    )

    book_repository.add_author(book_id=first_book_id, author_id=author_id)
    book_repository.add_author(book_id=second_book_id, author_id=author_id)

    result = book_repository.search_by_author("ROL")

    assert result == []


def test_search_by_author_matches_last_name(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Repository should find books by partial author last name."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="Fantasy novel",
        )
    )

    author_id = author_repository.add(
        AuthorModel(
            first_name="Dima",
            last_name="Tennessee",
            birth_date=date(1999, 1, 1),
        )
    )

    book_repository.add_author(book_id, author_id)

    books = book_repository.search_by_author("NES")

    assert [book.id for book in books] == [book_id]


def test_search_by_genre_is_partial_and_case_insensitive(
    book_repository: BookRepository,
    genre_repository: GenreRepository,
) -> None:
    """Repository should find books by partial genre name case-insensitively."""

    _ = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    second_book_id = book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    third_book_id = book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))
    genre_id = genre_repository.add(GenreModel(name="Some Some"))

    book_repository.add_genre(third_book_id, genre_id)
    book_repository.add_genre(second_book_id, genre_id)

    books = book_repository.search_by_genre("SO")

    assert len(books) == 2
    assert [item.id for item in books] == [second_book_id, third_book_id]


def test_search_by_genre_returns_empty_list_when_no_matches(
    book_repository: BookRepository,
    genre_repository: GenreRepository,
) -> None:
    """Repository should return an empty list when no genre matches."""

    _ = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="The Fantasy about geralt from rivia",
        ))
    second_book_id = book_repository.add(
        BookModel(
            title="Clean code",
            year=1999,
            description="A book about clean code",
        ))
    third_book_id = book_repository.add(
        BookModel(
            title="Python jun code",
            year=1989,
            description="A book about Python june code",
        ))
    genre_id = genre_repository.add(GenreModel(name="Some Some"))

    book_repository.add_genre(third_book_id, genre_id)
    book_repository.add_genre(second_book_id, genre_id)

    books = book_repository.search_by_genre("ROle")

    assert books == []


def test_deleting_book_removes_author_relation(
    book_repository: BookRepository,
    author_repository: AuthorRepository,
) -> None:
    """Deleting a book should remove its author relation."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="Fantasy novel",
        )
    )
    author_id = author_repository.add(
        AuthorModel(
            first_name="Dima",
            last_name="Tennessee",
            birth_date=date(1999, 1, 1),
        )
    )

    book_repository.add_author(book_id, author_id)
    book_repository.delete(book_id)

    assert author_repository.get_by_id(author_id) is not None
    assert author_repository.get_books(author_id) == []


def test_deleting_book_removes_genre_relation(
    book_repository: BookRepository,
    genre_repository: GenreRepository,
) -> None:
    """Deleting a book should remove its genre relation."""

    book_id = book_repository.add(
        BookModel(
            title="The Witcher",
            year=1999,
            description="Fantasy novel",
        )
    )
    genre_id = genre_repository.add(GenreModel(name="Fantasy"))

    book_repository.add_genre(book_id, genre_id)
    book_repository.delete(book_id)

    assert genre_repository.get_by_id(genre_id) is not None
    assert genre_repository.get_books(genre_id) == []
