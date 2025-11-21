#!/bin/bash
# Startup script for QA Agent System (Linux/Mac)

echo "========================================"
echo "   QA Agent System Startup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run: python -m venv venv"
    echo "Then activate and install requirements."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create .env from .env.example and add your API keys."
    echo ""
fi

echo "[INFO] Activating virtual environment..."
source venv/bin/activate

echo "[INFO] Starting FastAPI Backend..."
echo ""

# Start FastAPI in background
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "[INFO] Starting Streamlit UI..."
echo ""

# Start Streamlit
streamlit run app.py &
STREAMLIT_PID=$!

echo ""
echo "========================================"
echo "   Both services are running"
echo "========================================"
echo ""
echo "FastAPI Backend: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Streamlit UI: http://localhost:8501"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Streamlit PID: $STREAMLIT_PID"
echo ""
echo "To stop the services:"
echo "kill $BACKEND_PID $STREAMLIT_PID"
echo ""

# Wait for user interrupt
wait
