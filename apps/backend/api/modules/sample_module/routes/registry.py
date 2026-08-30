"""Register HTTP routes for sample_module."""

from fastapi import APIRouter

from modules.sample_module.routes.endpoints import get_hello, get_sample_items

router = APIRouter(prefix="/sample", tags=["sample"])
router.include_router(get_hello.router)
router.include_router(get_sample_items.router)
