"""Primary-key `id` column mixin for ORM models."""

import uuid

from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column


class IdModelMixin:
    """UUID primary key named `id` (generated in Python via uuid4)."""

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
