"""GET /sample/items — read sample rows from Postgres via ORM."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.db import get_db
from modules.sample_module.public.facades import SampleItemFacade
from modules.sample_module.routes.responses import SampleItemResponse

router = APIRouter()


@router.get("/items", response_model=list[SampleItemResponse])
def get_sample_items(
    db: Annotated[Session, Depends(get_db)],
) -> list[SampleItemResponse]:
    items = SampleItemFacade.list_items(db)
    return [
        SampleItemResponse(
            id=item.id,
            message=item.message,
        )
        for item in items
    ]
