"""Tests for GenreRepository."""

import pytest
from sqlalchemy.exc import IntegrityError

from models import BookModel
from models.genre_model import GenreModel

from repositories.genres import GenreRepository
from repositories.books import BookRepository


def test_add_and_get_by_id(
        genre_repository: GenreRepository
) -> None:
    """Test adding and getting a genre by id."""

    genre = GenreModel(
        name="Fantasy",
    )

    genre_id = genre_repository.add(genre)
    saved_genre = genre_repository.get_by_id(genre_id)

    assert genre_id > 0
    assert saved_genre is not None
    assert saved_genre.id == genre_id
    assert saved_genre.name == "Fantasy"


def test_get_all_returns_genres_ordered_by_name(
    genre_repository: GenreRepository,
) -> None:
    """Test getting all genres by name."""

    genre_science = genre_repository.add(GenreModel(name="Science Fiction"))
    genre_fantasy = genre_repository.add(GenreModel(name="Fantasy"))
    genre_drama = genre_repository.add(GenreModel(name="Drama"))

    genres = genre_repository.get_all()

    assert len(genres) == 3
    assert [genre.id for genre in genres] == [genre_drama, genre_fantasy, genre_science]


def test_update_existing_genre(
        genre_repository: GenreRepository,
) -> None:
    """Repository should update an existing genre."""

    genre_id = genre_repository.add(
        GenreModel(
            name="Fantasy"
        )
    )

    updated_genre = GenreModel(
        id=genre_id,
        name="Drama"
    )

    result = genre_repository.update(updated_genre)
    saved_genre = genre_repository.get_by_id(genre_id)

    assert result is True
    assert saved_genre is not None
    assert saved_genre.name == "Drama"
    assert saved_genre.id == genre_id


def test_update_returns_false_for_missing_genre(
        genre_repository: GenreRepository,
) -> None:
    """Repository should not update genre that does not exist."""

    genre_model = GenreModel(
        id=999,
        name="Unknown"
    )

    result = genre_repository.update(genre_model)

    assert result is False


def test_update_returns_false_when_genre_has_no_id(
        genre_repository: GenreRepository
) -> None:
    """Repository should not update genre that has no id."""

    genre_model = GenreModel(
        name="Fantasy"
    )

    result = genre_repository.update(genre_model)

    assert result is False


def test_delete_existing_genre(
    genre_repository: GenreRepository,
) -> None:
    """Repository should delete an existing genre."""

    genre_id = genre_repository.add(
        GenreModel(
            name="Fantasy"
        )
    )

    result = genre_repository.delete(genre_id)

    assert result is True
    assert genre_repository.get_by_id(genre_id) is None


def test_delete_returns_false_for_missing_genre(
    genre_repository: GenreRepository,
) -> None:
    """Repository should not delete genre that does not exist."""

    result = genre_repository.delete(999)

    assert result is False


def test_get_by_name_returns_exact_match(
    genre_repository: GenreRepository,
) -> None:
    """Test getting a genre by name."""

    genre_repository.add(GenreModel(name="Fantasy"))
    genre_repository.add(GenreModel(name="Drama"))
    genre_repository.add(GenreModel(name="Dark Fantasy"))

    genres = genre_repository.get_by_name("Fantasy")

    assert len(genres) == 1
    assert genres[0].name == "Fantasy"


def test_get_by_name_returns_empty_list_when_genre_is_missing(
    genre_repository: GenreRepository,
) -> None:
    """Test getting a genre by name that does not exist."""

    genre_repository.add(GenreModel(name="Fantasy"))
    genre_repository.add(GenreModel(name="Drama"))
    genre_repository.add(GenreModel(name="Dark Fantasy"))

    genres = genre_repository.get_by_name("Horror")

    assert len(genres) == 0
    assert genres == []


def test_search_by_name_is_partial_and_case_insensitive(
    genre_repository: GenreRepository,
) -> None:
    """Test searching by name with partial and case-insensitive."""

    genre_repository.add(GenreModel(name="Fantasy"))
    genre_repository.add(GenreModel(name="Drama"))
    genre_repository.add(GenreModel(name="Dark Fantasy"))
    genre_repository.add(GenreModel(name="Horror"))

    genres = genre_repository.search_by_name("FANT")

    assert len(genres) == 2
    assert [item.name for item in genres] == ["Fantasy", "Dark Fantasy"]


def test_search_by_name_returns_empty_list_when_no_matches(
    genre_repository: GenreRepository,
) -> None:
    """Test searching by name with no matches."""

    genre_repository.add(GenreModel(name="Fantasy"))
    genre_repository.add(GenreModel(name="Drama"))
    genre_repository.add(GenreModel(name="Dark Fantasy"))

    genres = genre_repository.search_by_name("Western")

    assert len(genres) == 0
    assert genres == []


def test_add_duplicate_genre_raises_integrity_error(
    genre_repository: GenreRepository,
) -> None:
    """Test adding duplicate genres."""

    first_genre_model = GenreModel(name="Fantasy")
    duplicate_genre_model = GenreModel(name="Fantasy")

    genre_repository.add(first_genre_model)

    with pytest.raises(IntegrityError):
        genre_repository.add(duplicate_genre_model)

    assert len(genre_repository.get_all()) == 1


def test_get_books_returns_books_assigned_to_genre(
    genre_repository: GenreRepository,
    book_repository: BookRepository,
) -> None:
    """Test getting books assigned to genre."""

    fantasy_id = genre_repository.add(GenreModel(name="Fantasy"))
    drama_id = genre_repository.add(GenreModel(name="Drama"))

    fantasy_book_id = book_repository.add(
        BookModel(
            title="The Hobbit",
            year=1937,
            description="Fantasy novel",
        )
    )

    drama_book_id = book_repository.add(
        BookModel(
            title="Hamlet",
            year=1603,
            description="Tragedy",
        )
    )

    book_repository.add_genre(fantasy_book_id, fantasy_id)
    book_repository.add_genre(drama_book_id, drama_id)

    books = genre_repository.get_books(fantasy_id)

    assert len(books) == 1
    assert books[0].title == "The Hobbit"


def test_get_books_returns_empty_list_when_genre_has_no_books(
    genre_repository: GenreRepository,
) -> None:
    """Repository should return an empty list for a genre without books."""

    genre_id = genre_repository.add(GenreModel(name="Fantasy"))

    books = genre_repository.get_books(genre_id)

    assert books == []


def test_get_books_returns_empty_list_for_missing_genre(
    genre_repository: GenreRepository,
) -> None:
    """Repository should return an empty list for a missing genre."""

    books = genre_repository.get_books(999)

    assert books == []
