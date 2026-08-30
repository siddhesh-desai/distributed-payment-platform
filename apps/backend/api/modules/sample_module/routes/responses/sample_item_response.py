"""HTTP response schemas for sample item routes (not table models)."""

from uuid import UUID

from pydantic import BaseModel, Field


class SampleItemResponse(BaseModel):
    id: UUID
    message: str = Field(min_length=1)
