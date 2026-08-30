"""ORM table shape for sample_items."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from payflow_common.models import IdModelMixin, OrmBaseModel


class SampleItem(IdModelMixin, OrmBaseModel):
    __tablename__ = "sample_items"

    message: Mapped[str] = mapped_column(String(255), nullable=False)
