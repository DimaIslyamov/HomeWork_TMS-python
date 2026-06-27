from library.cli.base import CrudDispatcher
from library.cli.helpers import read_input, read_int
from library.repositories.books import BookRepository
from library.models.entities import Book


class BookMenuDispatcher(CrudDispatcher):

    def __init__(self, repo: BookRepository):
        self._repo = repo


    @property
    def _title(self) -> str:
        return "Book"

    def _add(self) -> None:
        title = read_input("Enter the title: ")
        year = read_int("Enter the year YYYY: ")
        description = read_input("Enter the description: ")

        book_id = self._repo.add(entity=Book(
            id=None,
            title=title,
            year=year,
            description=description
        ))
        print(f"Book with id: {book_id} added")

    def _list_all(self) -> None:
        items = self._repo.get_all()

        if not items:
            print("No books found")
            return

        for item in items:
            print(f"{item.id}. "
                  f"{item.title} "
                  f"{item.year} "
                  f"{item.description}")

    def _find(self) -> None:
        pattern = read_input("Enter the Book name or part of name: ")
        book = self._repo.search_by_name(pattern)

        if not book:
            print("No book found")
            return

        for item in book:
            print(f"{item.id}. "
                  f"{item.title} "
                  f"{item.year} "
                  f"{item.description}")

    def _edit(self) -> None:
        book_id = read_int("Enter the Book ID: ")

        if book_id is None:
            return

        item = self._repo.get_by_id(book_id)

        if item is None:
            print(f"Book with id={book_id} not found")
            return

        title = read_input(
            "Enter the Book title: ",
            required=False) or item.title
        year = read_int(
            "Enter the Book year: ",
            required=False) or item.year
        description = read_input(
            "Enter the Book description: ",
            required=False) or item.description

        update_book = Book(
            id=book_id,
            title=title,
            year=year,
            description=description
        )

        if self._repo.update(entity=update_book):
            print("Book updated")
        else:
            print("Book not updated")

    def _delete(self) -> None:
        book_id = read_int("Enter the Book ID: ")

        if book_id is None:
            return

        if self._repo.delete(book_id):
            print("Book deleted")
        else:
            print("Book not deleted")

    def add_author_to_book(self) -> None:
        pass

    def add_genre_to_book(self) -> None:
        pass

    def show_authors(self) -> None:
        pass

    def show_genres(self) -> None:
        pass