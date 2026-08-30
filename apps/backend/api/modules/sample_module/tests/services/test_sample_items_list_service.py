"""SampleItemsListService unit tests.

- Lists sample items returned by the composed repository
"""

from unittest.mock import MagicMock, patch
from uuid import UUID

from modules.sample_module.models import SampleItem
from modules.sample_module.services import SampleItemsListService

_SEED_ID = UUID("11111111-1111-1111-1111-111111111111")


class _FakeSampleItemRepository:
    def list_all(self) -> list[SampleItem]:
        return [SampleItem(id=_SEED_ID, message="Hello from Postgres")]


def test_list_items_returns_repository_rows() -> None:
    with patch(
        "modules.sample_module.services.sample_items_list_service.SampleItemRepository",
        return_value=_FakeSampleItemRepository(),
    ):
        service = SampleItemsListService(MagicMock())
        items = service.list_items()

    assert len(items) == 1
    assert items[0].id == _SEED_ID
    assert items[0].message == "Hello from Postgres"
