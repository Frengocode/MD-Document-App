#!/usr/bin/bash
set -e

uv run alembic upgrade head &

uv run uvicorn src.application.app.app:app \
  --host 0.0.0.0 \
  --port 8000
