"""Support functions for CLI"""

from datetime import date
from typing import Optional


def read_input(prompt: str, required: bool = True) -> str:
    """Read input from user."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required.")


def read_int(prompt: str, required: bool = True) -> Optional[int]:
    """Read int value from user."""
    while True:
        value = read_input(prompt, required=required)
        if not value and not required:
            return None
        try:
            return int(value)
        except ValueError:
            print("Enter an integer.")


def read_required_int(prompt: str) -> int | None:
    """Convert string to int."""
    value = read_int(prompt=prompt, required=True)
    if value is None:
        raise RuntimeError("Required int cannot be None.")
    return value


def read_float(prompt: str) -> float:
    """Read a floating-point number from the user."""
    while True:
        value = read_input(prompt)
        try:
            number = float(value.replace(",", "."))
            return number
        except ValueError:
            print("Enter a number.")


def read_date(prompt: str, required: bool = False) -> Optional[date]:
    """Read the date in the YYYY-MM-DD format."""
    while True:
        value = read_input(
            f"{prompt} (YYYY-MM-DD, Enter — skip): ",
            required=required,
        )
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError:
            print("Incorrect date format. Please use YYYY-MM-DD.")


def pause() -> None:
    """A pause before returning to the menu."""
    input("\nPress Enter to continue....")