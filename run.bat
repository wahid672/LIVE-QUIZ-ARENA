@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Membuat virtual environment...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo Gagal membuat virtual environment. Pastikan Python 3.11+ terpasang.
        pause
        exit /b 1
    )
    echo [SETUP] Menginstal dependency...
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Gagal menginstal dependency.
        pause
        exit /b 1
    )
)

echo [RUN] Menjalankan LIVE QUIZ ARENA...
".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

if errorlevel 1 pause
endlocal
