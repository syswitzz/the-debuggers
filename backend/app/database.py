"""SQLite database setup and request-scoped sessions."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


class Base(DeclarativeBase):
    """Base class for all database models."""


def get_db() -> Generator[Session, None, None]:
    """Provide one database session per request and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
