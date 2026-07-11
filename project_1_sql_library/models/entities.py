"""Data models for library."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Author:
    """Data model for an author."""
    id: Optional[int]
    first_name: str
    last_name: str
    birth_date: Optional[date]

@dataclass
class Genre:
    """Data model for genre."""
    id: Optional[int]
    name: str

@dataclass
class Book:
    """Data model for book."""
    id: Optional[int]
    title: str
    year: int
    description: str
