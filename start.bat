@echo off
REM Startup script for QA Agent System (Windows)

echo ========================================
echo    QA Agent System Startup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then activate and install requirements.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env from .env.example and add your API keys.
    echo.
    pause
)

echo [INFO] Starting FastAPI Backend...
echo.

REM Start FastAPI in a new window
start "FastAPI Backend" cmd /k "venv\Scripts\activate && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

echo [INFO] Starting Streamlit UI...
echo.

REM Start Streamlit in a new window
start "Streamlit UI" cmd /k "venv\Scripts\activate && streamlit run app.py"

echo.
echo ========================================
echo    Both services are starting...
echo ========================================
echo.
echo FastAPI Backend: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Streamlit UI: http://localhost:8501
echo.
echo Press any key to close this window...
echo (The services will continue running)
echo.
pause > nul
