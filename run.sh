#!/usr/bin/env bash
set -eo pipefail
cd "$(dirname "$0")"

# 1. Cari binary Python >= 3.11 yang tersedia di sistem
PYTHON_BIN=""
for candidate in python3.13 python3.12 python3.11 python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
            PYTHON_BIN="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "[ERROR] Python 3.11 atau lebih baru tidak ditemukan di sistem ini."
    echo "Di Ubuntu/Debian/Kali Linux, jalankan:"
    echo "  sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    exit 1
fi

PY_VER=$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "[OK] Menggunakan Python: $PYTHON_BIN ($PY_VER)"

# 2. Tangani folder .venv (bersihkan jika sebelumnya dibuat di Windows / tidak ada bin/python)
if [ -d ".venv" ] && [ ! -x ".venv/bin/python" ]; then
    echo "[SETUP] Menghapus folder .venv lama (incompatible dari Windows/OS lain)..."
    rm -rf .venv
fi

# 3. Buat virtual environment jika belum ada
if [ ! -d ".venv" ]; then
    echo "[SETUP] Membuat virtual environment baru..."
    if ! "$PYTHON_BIN" -m venv .venv; then
        echo ""
        echo "[ERROR] Gagal membuat virtual environment (.venv)."
        echo "Di Ubuntu/Debian/Kali Linux, pastikan paket python3-venv terpasang:"
        echo "  sudo apt update && sudo apt install -y python3-venv python3-pip"
        exit 1
    fi
fi

# 4. Pastikan binary python di venv valid
if [ ! -x ".venv/bin/python" ]; then
    echo "[ERROR] Binary .venv/bin/python tidak ditemukan."
    exit 1
fi

# 5. Pasang / update dependency
echo "[SETUP] Memeriksa dependency..."
".venv/bin/python" -m pip install --upgrade pip --quiet 2>/dev/null || true
".venv/bin/python" -m pip install -r requirements.txt

# 6. Jalankan server LIVE QUIZ ARENA
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"

echo ""
echo "=========================================================="
echo "  LIVE QUIZ ARENA BERJALAN DI http://$HOST:$PORT"
echo "  - Dashboard : http://localhost:$PORT/dashboard"
echo "  - Overlay   : http://localhost:$PORT/overlay"
echo "=========================================================="
echo ""

exec ".venv/bin/python" -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
