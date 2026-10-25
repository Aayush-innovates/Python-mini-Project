@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  python -m venv .venv
  if errorlevel 1 (
    echo Failed to create venv. Is Python installed?
    pause
    exit /b 1
  )
  .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo Starting LogicFlow...
.venv\Scripts\python.exe -m streamlit run app.py
pause
