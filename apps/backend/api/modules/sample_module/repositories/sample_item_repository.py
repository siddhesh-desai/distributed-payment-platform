"""Persistence for SampleItem rows."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modules.sample_module.models import SampleItem
from payflow_common.repositories import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class SampleItemRepository(BaseRepository[SampleItem]):
    """Loads sample items via shared list helpers (constructor DI)."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, model_type=SampleItem)
