"""Session factory and FastAPI request-scoped DB dependency."""

from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING

from sqlalchemy.orm import sessionmaker

from core.db.engine import engine

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Yield one Session per request; roll back on error; always close."""
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
