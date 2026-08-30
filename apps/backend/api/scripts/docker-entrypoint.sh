#!/bin/sh
set -eu

alembic -c core/alembic/alembic.ini upgrade heads
exec uvicorn main:app --host 0.0.0.0 --port 8000
