# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /usr/local/bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Workspace root + every [tool.uv.workspace] member payflow-api depends on.
COPY pyproject.toml uv.lock ./
COPY apps/backend/api ./apps/backend/api
COPY libs/backend ./libs/backend

RUN uv sync --frozen --package payflow-api --no-dev \
    && chmod +x /app/apps/backend/api/scripts/docker-entrypoint.sh

WORKDIR /app/apps/backend/api

EXPOSE 8000

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
