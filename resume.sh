#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

python -m venv .venv

# Git Bash / MSYS on Windows puts the interpreter in Scripts/, POSIX in bin/
if [ -x ".venv/Scripts/python.exe" ]; then
    VENV_PY=".venv/Scripts/python.exe"
else
    VENV_PY=".venv/bin/python"
fi

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt

if [ ! -f .env ] && [ -f .env.example ]; then
    cp .env.example .env
    echo "Created .env from .env.example — add your API keys before going public."
fi

export PYTHONPATH="$(pwd)"
exec "$VENV_PY" -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
