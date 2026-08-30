"""HTTP response schemas for sample_module hello routes (not table models)."""

from pydantic import BaseModel, Field


class HelloResponse(BaseModel):
    message: str = Field(min_length=1)
    module: str = Field(min_length=1)
