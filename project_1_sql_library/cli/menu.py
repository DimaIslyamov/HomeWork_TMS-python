"""Console menu for library."""

from sqlalchemy.orm import Session

from cli.author_menu import AuthorMenuDispatcher
from cli.genre_menu import GenreMenuDispatcher
from cli.book_menu import BookMenuDispatcher
from cli.helpers import read_input
from repositories.genres import GenreRepository
from repositories.books import BookRepository
from repositories.authors import AuthorRepository


class MainMenu:
    """Main menu for all project."""

    def __init__(self, session: Session) -> None:
        author_repository = AuthorRepository(session)
        genre_repository = GenreRepository(session)
        book_repository = BookRepository(session)

        self._author_menu = AuthorMenuDispatcher(author_repository)
        self._genre_menu = GenreMenuDispatcher(genre_repository)
        self._book_menu = BookMenuDispatcher(book_repository)

    def run_menu(self) -> None:
        """Started main cycle of application."""
        print("==== Library Menu ====")
        while True:
            self._print_main_menu()
            choice = read_input("Enter choice: ")

            if choice in ('0', 'exit'):
                print("Exiting...")
                break

            self._dispatch(choice)

    @staticmethod
    def _print_main_menu() -> None:
        print("---- Main Menu ----")
        print("1. Authors")
        print("2. Genres")
        print("3. Books")
        print("0. Exit")

    def _dispatch(self, choice: str) -> None:
        handlers = {
            '1': self._author_menu.run,
            '2': self._genre_menu.run,
            '3': self._book_menu.run,
        }

        handler = handlers.get(choice)

        if handler:
            handler()
        else:
            print("Invalid choice.")
