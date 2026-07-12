from cli.base import CrudDispatcher
from cli.helpers import read_input, read_int
from repositories.genres import GenreRepository
from models.genre_model import GenreModel


class GenreMenuDispatcher(CrudDispatcher):

    def __init__(self, repo: GenreRepository):
        self._repo = repo

    @property
    def _title(self) -> str:
        return "Genre"

    def _add(self) -> None:
        name = read_input("Enter the Genre: ")
        genre_id = self._repo.add(
            GenreModel(
                name=name
            )
        )
        print(f"Genre for {genre_id} was added")

    def _list_all(self) -> None:
        items = self._repo.get_all()

        for genre in items:
            print(f"{genre.id}. "
                  f"{genre.name.title()}")

    def _find(self) -> None:
        pattern = read_input("Enter Genre name or part of name: ")
        genres = self._repo.search_by_name(pattern)

        if not genres:
            print("Genre not found")
            return

        for genre in genres:
            print(f"{genre.id}. "
                  f"{genre.name.title()}")

    def _edit(self) -> None:
        genre_id = read_int("Enter the Genre ID: ")

        if genre_id is None:
            return

        item = self._repo.get_by_id(genre_id)

        if item is None:
            print(f"Genre with id={genre_id} not found")
            return

        name = read_input(
            "Enter the Genre new name: ",
            required=False) or item.name

        item.name = name

        if self._repo.update(item):
            print("Genre updated")
        else:
            print("Genre not found")

    def _delete(self) -> None:
        genre_id = read_int("Enter the Genre ID: ")

        if genre_id is None:
            return

        if self._repo.delete(genre_id):
            print("Genre deleted")
        else:
            print("Genre not found")

    def show_books(self) -> None:
        genre_id = read_int("Enter the Genre ID: ")

        if genre_id is None:
            return

        genre = self._repo.get_by_id(genre_id)

        if genre is None:
            print(f"Genre with id={genre_id} not found")
            return

        books = self._repo.get_books(genre_id)
        if not books:
            print("No books found")
            return

        print(f"Books by {genre.id} {genre.name}.")

        for book in books:
            print(
                f"{book.id}. "
                f"{book.title.title()} "
                f"{book.year} - "
                f"{book.description}"
            )
