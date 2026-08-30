"""OrmBaseModel accepts mixins and registers mapped columns.

- Composes IdModelMixin with OrmBaseModel so the mapped table exposes an id PK
"""

from payflow_common.models import IdModelMixin, OrmBaseModel


def test_orm_base_composes_with_id_mixin() -> None:
    class _Row(IdModelMixin, OrmBaseModel):
        __tablename__ = "orm_base_compose_smoke"

    assert "id" in _Row.__table__.c
    assert _Row.__table__.c.id.primary_key
