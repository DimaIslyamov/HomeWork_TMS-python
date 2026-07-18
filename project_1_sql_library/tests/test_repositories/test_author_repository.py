"""Tests for AuthorRepository."""

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from models.author_model import AuthorModel
from repositories.authors import AuthorRepository


def test_add_and_get_by_id(
    author_repository: AuthorRepository,
) -> None:
    """Repository should add an author and return it by id."""

    author = AuthorModel(
        first_name="Robert",
        last_name="Martin",
        birth_date=date(1952, 12, 5),
    )

    author_id = author_repository.add(author)
    saved_author = author_repository.get_by_id(author_id)

    assert author_id > 0
    assert saved_author is not None
    assert saved_author.id == author_id
    assert saved_author.first_name == "Robert"
    assert saved_author.last_name == "Martin"
    assert saved_author.birth_date == date(1952, 12, 5)


def test_get_by_id_returns_none_for_missing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return None when author does not exist."""

    author = author_repository.get_by_id(999)

    assert author is None


def test_get_all_returns_authors_ordered_by_id(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return all authors ordered by id."""

    first_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )
    second_id = author_repository.add(
        AuthorModel(
            first_name="Martin",
            last_name="Fowler",
            birth_date=date(1963, 12, 18),
        )
    )

    authors = author_repository.get_all()

    assert len(authors) == 2
    assert [author.id for author in authors] == [first_id, second_id]


def test_update_existing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should update an existing author."""

    author_id = author_repository.add(
        AuthorModel(
            first_name="Bob",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )

    updated_author = AuthorModel(
        id=author_id,
        first_name="Robert",
        last_name="Martin",
        birth_date=date(1952, 12, 5),
    )

    result = author_repository.update(updated_author)
    saved_author = author_repository.get_by_id(author_id)

    assert result is True
    assert saved_author is not None
    assert saved_author.first_name == "Robert"


def test_update_returns_false_for_missing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should not update an author that does not exist."""

    author = AuthorModel(
        id=999,
        first_name="Unknown",
        last_name="Author",
        birth_date=None,
    )

    result = author_repository.update(author)

    assert result is False


def test_update_returns_false_when_author_has_no_id(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return False when author has no id."""

    author = AuthorModel(
        first_name="Robert",
        last_name="Martin",
        birth_date=date(1952, 12, 5),
    )

    result = author_repository.update(author)

    assert result is False


def test_delete_existing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should delete an existing author."""

    author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )

    result = author_repository.delete(author_id)

    assert result is True
    assert author_repository.get_by_id(author_id) is None


def test_delete_returns_false_for_missing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return False when author does not exist."""

    result = author_repository.delete(999)

    assert result is False


def test_get_by_name_matches_first_or_last_name(
    author_repository: AuthorRepository,
) -> None:
    """Repository should find authors by exact first or last name."""

    author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )
    author_repository.add(
        AuthorModel(
            first_name="Martin",
            last_name="Fowler",
            birth_date=date(1963, 12, 18),
        )
    )

    authors = author_repository.get_by_name("Martin")

    assert len(authors) == 2
    assert {author.last_name for author in authors} == {
        "Martin",
        "Fowler",
    }


def test_get_by_name_returns_empty_list_when_no_matches(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return an empty list when exact name is missing."""

    author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )

    authors = author_repository.get_by_name("Unknown")

    assert authors == []


def test_search_by_name_is_partial_and_case_insensitive(
    author_repository: AuthorRepository,
) -> None:
    """Search should support partial case-insensitive matching."""

    author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )
    author_repository.add(
        AuthorModel(
            first_name="Martin",
            last_name="Fowler",
            birth_date=date(1963, 12, 18),
        )
    )

    authors = author_repository.search_by_name("MART")

    assert len(authors) == 2


def test_search_by_name_returns_empty_list_when_no_matches(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return an empty list when no partial name matches."""

    author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )

    authors = author_repository.search_by_name("ZZZ")

    assert authors == []


def test_add_duplicate_author_raises_integrity_error(
    author_repository: AuthorRepository,
) -> None:
    """Repository should reject duplicate authors."""

    first_author = AuthorModel(
        first_name="Robert",
        last_name="Martin",
        birth_date=date(1952, 12, 5),
    )
    duplicate_author = AuthorModel(
        first_name="Robert",
        last_name="Martin",
        birth_date=date(1952, 12, 5),
    )

    author_repository.add(first_author)

    with pytest.raises(IntegrityError):
        author_repository.add(duplicate_author)

    assert len(author_repository.get_all()) == 1


def test_get_books_returns_empty_list_when_author_has_no_books(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return an empty list for an author without books."""

    author_id = author_repository.add(
        AuthorModel(
            first_name="Robert",
            last_name="Martin",
            birth_date=date(1952, 12, 5),
        )
    )

    books = author_repository.get_books(author_id)

    assert books == []


def test_get_books_returns_empty_list_for_missing_author(
    author_repository: AuthorRepository,
) -> None:
    """Repository should return an empty list for a missing author."""

    books = author_repository.get_books(999)

    assert books == []
