"""List sample items use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modules.sample_module.repositories import SampleItemRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from modules.sample_module.models import SampleItem


class SampleItemsListService:
    """Lists sample items; composes repositories from the request db session."""

    def __init__(self, db: Session) -> None:
        self._sample_items = SampleItemRepository(db)

    def list_items(self) -> list[SampleItem]:
        return self._sample_items.list_all()
