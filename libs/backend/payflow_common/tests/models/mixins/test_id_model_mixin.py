"""IdModelMixin provides a UUID primary key named id.

- Adds a UUID primary key column named id with a client-side uuid4 default
"""

from sqlalchemy import Uuid

from payflow_common.models import IdModelMixin, OrmBaseModel


def test_id_model_mixin_adds_uuid_primary_key() -> None:
    class _Row(IdModelMixin, OrmBaseModel):
        __tablename__ = "id_mixin_smoke"

    col = _Row.__table__.c.id
    assert col.primary_key
    assert isinstance(col.type, Uuid)
    assert col.default is not None
