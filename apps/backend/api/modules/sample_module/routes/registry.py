"""Register HTTP routes for sample_module."""

from fastapi import APIRouter

from modules.sample_module.routes.endpoints import get_hello

router = APIRouter(prefix="/sample", tags=["sample"])
router.include_router(get_hello.router)
