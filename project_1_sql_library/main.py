"""Entry point into the library application."""

from database.session import SessionFactory
from cli.menu import MainMenu


def main() -> None:
    """Run library application."""
    with SessionFactory() as session:
        menu = MainMenu(session)
        menu.run_menu()


if __name__ == "__main__":
    main()
