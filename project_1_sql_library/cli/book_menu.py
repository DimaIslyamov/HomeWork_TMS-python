from cli.base import CrudDispatcher
from cli.helpers import (
    read_input,
    read_int,
    read_required_int
)
from repositories.books import BookRepository
from models.entities import Book


class BookMenuDispatcher(CrudDispatcher):

    def __init__(self, repo: BookRepository):
        self._repo = repo


    @property
    def _title(self) -> str:
        return "Book"

    def _add(self) -> None:
        title = read_input("Enter the title: ")
        year = read_required_int("Enter the year YYYY: ")
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

    def run(self) -> None:
        while True:
            print(f"\n--- {self._title} ---")
            print("1. Add book")
            print("2. Show all books")
            print("3. Find book")
            print("4. Edit book")
            print("5. Delete book")
            print("6. Add author to book")
            print("7. Add genre to book")
            print("8. Show book authors")
            print("9. Show book genres")
            print("10. Search by author")
            print("11. Search by genre")
            print("0. Back")

            choice = read_input("Enter choice: ")

            if choice == "1":
                self._add()
            elif choice == "2":
                self._list_all()
            elif choice == "3":
                self._find()
            elif choice == "4":
                self._edit()
            elif choice == "5":
                self._delete()
            elif choice == "6":
                self.add_author_to_book()
            elif choice == "7":
                self.add_genre_to_book()
            elif choice == "8":
                self.show_authors()
            elif choice == "9":
                self.show_genres()
            elif choice == "10":
                self._search_by_author()
            elif choice == "11":
                self._search_by_genre()
            elif choice == "0":
                return
            else:
                print("Invalid choice.")

    def add_author_to_book(self) -> None:
        book_id = read_int("Enter the Book ID: ")
        if book_id is None:
            return

        author_id = read_int("Enter the Author ID: ")
        if author_id is None:
            return

        if self._repo.add_author(
            book_id=book_id,
            author_id=author_id
        ):
            print("Author added to book")
        else:
            print("Author not added to book")

    def add_genre_to_book(self) -> None:
        book_id = read_int("Enter the Book ID: ")
        if book_id is None:
            return

        genre_id = read_int("Enter the Genre ID: ")
        if genre_id is None:
            return

        if self._repo.add_genre(
            book_id=book_id,
            genre_id=genre_id
        ):
            print("Genre added to book")
        else:
            print("Genre not added to book")

    def show_authors(self) -> None:
        book_id = read_int("Enter the Book ID: ")
        if book_id is None:
            return

        book = self._repo.get_by_id(book_id)
        if book is None:
            print("Book not found.")
            return

        authors = self._repo.get_authors(book_id)

        if not authors:
            print("No authors found for this book.")
            return

        print(f"Authors of {book.title}:")

        for author in authors:
            print(
                f"{author.id}. "
                f"{author.first_name.title()} "
                f"{author.last_name.title()} "
                f"{author.birth_date}"
            )

    def show_genres(self) -> None:
        book_id = read_int("Enter the Book ID: ")
        if book_id is None:
            return

        book = self._repo.get_by_id(book_id)
        if book is None:
            print("Book not found.")
            return

        genres = self._repo.get_genres(book_id)

        if not genres:
            print("No genres found for this book.")
            return

        print(f"Genres of {book.title}:")

        for genre in genres:
            print(f"{genre.id}. {genre.name.title()}")

    def _search_by_author(self) -> None:
        author_name = read_input("Enter the Author: ")
        books = self._repo.search_by_author(author_name)

        if not books:
            print("No books found for this author.")
            return

        for book in books:
            print(f"{book.id}. {book.title} - {book.year}: {book.description}")

    def _search_by_genre(self) -> None:
        genre_name = read_input("Enter the Genre: ")
        books = self._repo.search_by_genre(genre_name)

        if not books:
            print("No books found for this genre.")
            return

        for book in books:
            print(f"{book.id}. {book.title} - {book.year}: {book.description}")
