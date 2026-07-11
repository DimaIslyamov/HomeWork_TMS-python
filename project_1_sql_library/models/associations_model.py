from sqlalchemy import Column, Integer, ForeignKey, Table

from database.base import Base


books_authors = Table(
    "books_authors",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey(
            "books.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "author_id",
        Integer,
        ForeignKey(
            "authors.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)

books_genres = Table(
    "books_genres",
    Base.metadata,
    Column(
        "book_id",
        Integer,
        ForeignKey(
            "books.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
    Column(
        "genre_id",
        Integer,
        ForeignKey(
            "genres.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)
