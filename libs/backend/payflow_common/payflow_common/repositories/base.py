"""Generic SQLAlchemy repository with shared CRUD helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BaseRepository[ModelT]:
    """Persistence helpers for one mapped model type.

    Bind a concrete mapped class via `model_type` and inject a unit-of-work
    `Session` as `db`. Subclasses add domain-specific queries; shared
    reads/writes live here as CRUD grows.
    """

    def __init__(self, db: Session, *, model_type: type[ModelT]) -> None:
        self._db = db
        self._model_type = model_type

    def list_all(self) -> list[ModelT]:
        """Return every row for this model."""
        return list(self._db.scalars(select(self._model_type)).all())
