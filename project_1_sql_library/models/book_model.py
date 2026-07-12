from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base
from models.associations_model import books_authors, books_genres

if TYPE_CHECKING:
    from models.author_model import AuthorModel
    from models.genre_model import GenreModel


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
        server_default="",
    )

    authors: Mapped[list["AuthorModel"]] = relationship(
        secondary=books_authors,
        back_populates="books",
    )

    genres: Mapped[list["GenreModel"]] = relationship(
        secondary=books_genres,
        back_populates="books",
    )
