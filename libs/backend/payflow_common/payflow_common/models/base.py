"""SQLAlchemy declarative base for PayFlow mapped classes."""

from sqlalchemy.orm import DeclarativeBase


class OrmBaseModel(DeclarativeBase):
    """Shared ORM base — inherit mixins + this class on domain models."""
