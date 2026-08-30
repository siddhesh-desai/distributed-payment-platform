"""SampleItemFacade unit tests.

- Lists sample items via the list use-case service
"""

from unittest.mock import MagicMock, patch
from uuid import UUID

from modules.sample_module.models import SampleItem
from modules.sample_module.public.facades import SampleItemFacade

_SEED_ID = UUID("11111111-1111-1111-1111-111111111111")
_LIST_SERVICE = ".".join(
    (
        "modules.sample_module.public.facades",
        "sample_item_facade",
        "SampleItemsListService",
    )
)


class _FakeSampleItemsListService:
    def list_items(self) -> list[SampleItem]:
        return [SampleItem(id=_SEED_ID, message="Hello from Postgres")]


def test_list_items_delegates_to_list_service() -> None:
    with patch(_LIST_SERVICE, return_value=_FakeSampleItemsListService()):
        items = SampleItemFacade.list_items(MagicMock())

    assert len(items) == 1
    assert items[0].id == _SEED_ID
    assert items[0].message == "Hello from Postgres"
