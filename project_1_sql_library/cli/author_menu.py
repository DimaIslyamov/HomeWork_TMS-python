from cli.base import CrudDispatcher
from cli.helpers import read_input, read_date, read_int
from repositories.authors import AuthorRepository
from models.author_model import AuthorModel


class AuthorMenuDispatcher(CrudDispatcher):

    def __init__(self, repo: AuthorRepository):
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Authors"

    def _add(self) -> None:
        first_name = read_input("Enter first name: ")
        last_name = read_input("Enter last name: ")
        birth_date = read_date("Enter date of birth", required=False)

        author_id = self._repo.add(
            AuthorModel(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
            )
        )

        print(f"Author with id={author_id} added")

    def _list_all(self) -> None:
        items = self._repo.get_all()

        if not items:
            print("No authors found.")
            return

        for item in items:
            print(f"{item.id}. "
                  f"{item.first_name.title()} "
                  f"{item.last_name.title()} "
                  f"{item.birth_date}")

    def _find(self) -> None:
        pattern = read_input("Enter author name or part of name: ")
        authors = self._repo.search_by_name(pattern)

        if not authors:
            print("No authors found.")
            return

        for author in authors:
            print(f"{author.id}. "
                  f"{author.first_name.title()} "
                  f"{author.last_name.title()} "
                  f"{author.birth_date}"
                  )

    def _edit(self) -> None:
        author_id = read_int("Enter author ID: ")

        if author_id is None:
            return

        item = self._repo.get_by_id(author_id)

        if item is None:
            print(f"Author with id={author_id} not found")
            return

        first_name = read_input(
            f"Enter first name {item.first_name.title()}: ",
            required=False) or item.first_name
        last_name = read_input(
            f"Enter last name {item.last_name.title()}: ",
            required=False) or item.last_name
        date_of_birth = read_date(
            f"Enter new birth/old is {item.birth_date}: ",
            required=False)

        if date_of_birth is None:
            date_of_birth = item.birth_date

        updated_author = AuthorModel(
            id=author_id,
            first_name=first_name,
            last_name=last_name,
            birth_date=date_of_birth
        )

        if self._repo.update(entity=updated_author):
            print("Author updated")
        else:
            print("Author not updated")

    def _delete(self) -> None:
        author_id = read_int("Enter author ID: ")

        if author_id is None:
            return

        if self._repo.delete(author_id):
            print("Author deleted")
        else:
            print("Author not deleted")

    def show_books(self) -> None:
        author_id = read_int("Enter author ID: ")

        if author_id is None:
            return

        author = self._repo.get_by_id(author_id)

        if author is None:
            print(f"Author with id={author_id} not found")
            return

        books = self._repo.get_books(author_id)
        if not books:
            print("No books found.")
            return

        print(f"Books by {author.first_name} {author.last_name} ")

        for book in books:
            print(
                f"{book.id}. "
                f"{book.title.title()} "
                f"{book.year} - "
                f"{book.description}"
            )
