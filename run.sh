#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PYTHON_BIN=""
if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "[ERROR] Python 3 tidak ditemukan. Instal Python 3.11 atau lebih baru."
    exit 1
fi

if ! "$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo "[ERROR] LIVE QUIZ ARENA membutuhkan Python 3.11 atau lebih baru."
    exit 1
fi

if [ ! -x ".venv/bin/python" ]; then
    echo "[SETUP] Membuat virtual environment..."
    "$PYTHON_BIN" -m venv .venv
fi

echo "[SETUP] Memasang dependency..."
".venv/bin/python" -m pip install --upgrade pip
".venv/bin/python" -m pip install -r requirements.txt

echo "[RUN] Menjalankan LIVE QUIZ ARENA..."
exec ".venv/bin/python" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
