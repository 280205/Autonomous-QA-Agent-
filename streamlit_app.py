"""
Combined FastAPI + Streamlit Application
Runs both backend API and frontend UI in one process
"""

import streamlit as st
from streamlit.web import cli as stcli
import sys
import threading
import uvicorn
from backend.main import app as fastapi_app


def run_backend():
    """Run FastAPI backend in a separate thread"""
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info")


if __name__ == "__main__":
    # Start FastAPI backend in background thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Run Streamlit frontend
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
