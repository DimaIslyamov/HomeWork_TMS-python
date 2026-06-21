"""Basic utilities for repositories."""

import sqlite3
from datetime import date
from typing import Optional


def require_lastrowid(cursor: sqlite3.Cursor) -> int:
    """Return the ID of the last inserted row."""
    row_id = cursor.lastrowid
    if row_id is None:
        raise RuntimeError("INSERT did not return a row id")
    return row_id


def matches_partial(text: str, pattern: str) -> bool:
    """Check for partial matches without considering case (including Cyrillic characters)."""
    return pattern.casefold() in text.casefold()


def parse_date(value: Optional[str]) -> Optional[date]:
    """Convert an ISO date string to a date object."""
    if not value:
        return None
    return date.fromisoformat(value)


def format_date(value: Optional[date]) -> Optional[str]:
    """Convert date to an ISO string"""
    if value is None:
        return None
    return value.isoformat()
