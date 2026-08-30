"""Published SampleItem operations for HTTP and other modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from modules.sample_module.services import SampleItemsListService

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from modules.sample_module.models import SampleItem


class SampleItemFacade:
    """Static facade over sample-item use-case services."""

    @staticmethod
    def list_items(db: Session) -> list[SampleItem]:
        return SampleItemsListService(db).list_items()
