"""Aggregate domain module routers into one API router."""

from fastapi import APIRouter

from modules.sample_module.routes.registry import router as sample_router

api_router = APIRouter()
api_router.include_router(sample_router)
