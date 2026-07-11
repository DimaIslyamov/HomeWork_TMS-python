"""SQLAlchemy session configuration."""

from sqlalchemy.orm import Session, sessionmaker

from library.database.engine import engine


SessionFactory: sessionmaker[Session] = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=True,
    expire_on_commit=False,
)
