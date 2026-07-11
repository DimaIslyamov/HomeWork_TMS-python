"""Entry point into the library application."""

from database.connection import Database
from cli.menu import MainMenu
from database.schema import init_schema


def main() -> None:
    """Run library application."""
    with Database() as db:
        init_schema(db)

        menu = MainMenu(db)
        menu.run_menu()


if __name__ == "__main__":
    main()
