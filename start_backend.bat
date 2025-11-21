@echo off
echo Starting FastAPI Backend...
set TF_ENABLE_ONEDNN_OPTS=0
set TRANSFORMERS_NO_TF=1
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
