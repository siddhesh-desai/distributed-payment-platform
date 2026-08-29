"""PayFlow product API entrypoint — composes domain module routers."""

from fastapi import FastAPI

from core.router_registry import api_router

app = FastAPI(title="PayFlow API", version="0.1.0")
app.include_router(api_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
