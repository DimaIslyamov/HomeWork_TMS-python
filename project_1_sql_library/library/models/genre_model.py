from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library.database.base import Base
from library.models.associations_model import books_genres

if TYPE_CHECKING:
    from library.models.book_model import BookModel


class GenreModel(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    books: Mapped[list["BookModel"]] = relationship(
        secondary=books_genres,
        back_populates="genres",
    )
