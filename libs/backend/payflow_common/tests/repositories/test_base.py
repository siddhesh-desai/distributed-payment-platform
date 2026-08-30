"""BaseRepository list_all use cases.

- Returns all mapped rows for the bound model
"""

from __future__ import annotations

from sqlalchemy import String, create_engine
from sqlalchemy.orm import Mapped, Session, mapped_column, sessionmaker

from payflow_common.models import IdModelMixin, OrmBaseModel
from payflow_common.repositories import BaseRepository


class _Item(IdModelMixin, OrmBaseModel):
    __tablename__ = "base_repository_items"

    message: Mapped[str] = mapped_column(String(64))


def test_list_all_returns_all_rows() -> None:
    engine = create_engine("sqlite:///:memory:")
    OrmBaseModel.metadata.create_all(engine)
    factory = sessionmaker(bind=engine)

    with Session(engine) as seed:
        seed.add_all(
            [
                _Item(message="second"),
                _Item(message="first"),
            ]
        )
        seed.commit()

    with factory() as db:
        repository = BaseRepository(db, model_type=_Item)
        rows = repository.list_all()

    assert len(rows) == 2
    assert {row.message for row in rows} == {"first", "second"}
