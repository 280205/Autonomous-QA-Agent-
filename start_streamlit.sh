#!/bin/bash
# Combined startup script for Streamlit Cloud
# Runs FastAPI backend in background and Streamlit frontend

# Start FastAPI backend in background
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
sleep 5

# Start Streamlit frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
