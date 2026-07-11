"""Entry point into the library application."""

from library.database.connection import Database
from library.cli.menu import MainMenu
from library.database.schema import init_schema


def main() -> None:
    """Run library application."""
    with Database() as db:
        init_schema(db)

        menu = MainMenu(db)
        menu.run_menu()


if __name__ == "__main__":
    main()
