from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library.database.base import Base
from library.models.associations_model import books_authors

if TYPE_CHECKING:
    from library.models.book_model import BookModel


class AuthorModel(Base):
    __tablename__ = 'authors'

    __table_args__ = (
        UniqueConstraint(
            'first_name',
            'last_name',
            'birth_date',
            name="uq_authors_full_name_birth_date",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=False)

    books: Mapped[list["BookModel"]] = relationship(
        secondary=books_authors,
        back_populates="authors",
    )
