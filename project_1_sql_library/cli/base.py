"""Base class for all CLI commands."""

from abc import ABC, abstractmethod

from cli.helpers import read_input


class CrudDispatcher(ABC):
    """Base dispatcher for CRUD menu."""

    @property
    @abstractmethod
    def _title(self) -> str:
        """Return title of menu."""

    @abstractmethod
    def _add(self) -> None:
        """Add object."""

    @abstractmethod
    def _list_all(self) -> None:
        """Show all objects."""

    @abstractmethod
    def _find(self) -> None:
        """Find object."""

    @abstractmethod
    def _edit(self) -> None:
        """Edit object."""

    @abstractmethod
    def _delete(self) -> None:
        """Delete object."""

    def run(self) -> None:
        while True:
            print(f"\n--- {self._title} ---")
            print("1. Add")
            print("2. Show all")
            print("3. Find")
            print("4. Edit")
            print("5. Delete")
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
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
