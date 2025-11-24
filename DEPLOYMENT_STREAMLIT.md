# 🚀 Deployment Guide - Streamlit Cloud (Free Tier)

## Quick Overview
This guide helps you deploy the QA Agent on Streamlit Cloud's free tier without hitting build size limits.

## Key Optimizations Made
✅ Removed heavy PyTorch dependency (sentence-transformers)
✅ Using OpenAI embeddings instead (lightweight)
✅ Optimized requirements to ~50MB (vs 900MB+ before)
✅ Single deployment (backend + frontend together)

---

## Prerequisites
1. GitHub account
2. OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
3. Streamlit Cloud account ([Sign up free](https://streamlit.io/cloud))

---

## Step 1: Switch to Lightweight Vector DB

Before deploying, switch to the OpenAI-based embeddings:

### Option A: Automatic (Recommended)
Run this command:
```bash
copy backend\vector_db_openai.py backend\vector_db.py
```

### Option B: Manual
1. Open `backend/vector_db.py`
2. Replace the entire content with `backend/vector_db_openai.py`

---

## Step 2: Push to GitHub

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Optimize for Streamlit Cloud deployment - use OpenAI embeddings"

# Push to GitHub
git push origin master
```

---

## Step 3: Deploy on Streamlit Cloud

### A. Go to Streamlit Cloud
1. Visit https://share.streamlit.io/
2. Sign in with GitHub
3. Click **"New app"**

### B. Configure App
- **Repository**: `280205/Autonomous-QA-Agent-`
- **Branch**: `master`
- **Main file path**: `app.py`

### C. Advanced Settings
Click "Advanced settings" and add:

**Python version**: `3.11`

**Secrets** (paste this in the text box):
```toml
OPENAI_API_KEY = "your-openai-api-key-here"
BACKEND_URL = "http://localhost:8000"
```

Replace `your-openai-api-key-here` with your actual OpenAI API key.

### D. Deploy
Click **"Deploy!"** and wait 3-5 minutes.

---

## Step 4: Start Backend Locally (For Development)

The backend runs locally while frontend is on Streamlit Cloud:

### Windows:
```bash
start_backend.bat
```

### Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Expected Build Size

**Before optimization**: ~900MB (❌ Too large for free tier)
**After optimization**: ~50-80MB (✅ Perfect for free tier)

### What we removed:
- ❌ `sentence-transformers` (~700MB - PyTorch)
- ❌ Heavy ML libraries
- ❌ Unnecessary dependencies

### What we kept:
- ✅ All functionality working
- ✅ OpenAI embeddings (better quality!)
- ✅ Document processing
- ✅ Test case generation
- ✅ Selenium script generation

---

## Troubleshooting

### Error: "Module not found: sentence_transformers"
**Solution**: You forgot Step 1. Replace `vector_db.py` with `vector_db_openai.py`.

### Error: "Build exceeded resource limits"
**Solution**: Make sure you're using `requirements-streamlit.txt` not `requirements.txt`.
Update your repo root to have correct requirements.

### Error: "OpenAI API key not found"
**Solution**: Add your API key in Streamlit Cloud secrets (Step 3C).

### Backend not connecting
**Solution**: 
- For local dev: Run `start_backend.bat`
- For production: Consider deploying backend separately (see Advanced section)

---

## Advanced: Deploy Backend Separately (Optional)

If you want backend also in cloud:

### Option 1: Railway.app (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Option 2: Render.com
- Use `render.yaml` configuration
- Set environment variables
- Deploy backend as web service

Then update `BACKEND_URL` in Streamlit secrets to your backend URL.

---

## Cost Estimate

**Streamlit Cloud**: FREE (500 MB, 1 CPU)
**Backend (local)**: FREE (runs on your machine)
**OpenAI API**: ~$0.0001 per 1K tokens (very cheap)

**Monthly cost**: ~$1-5 depending on usage

---

## Support

If you face issues:
1. Check Streamlit logs: Click "Manage app" → "Logs"
2. Verify OpenAI API key is correct
3. Ensure backend is running locally
4. Check GitHub repo has latest code

---

## Next Steps

✅ App deployed successfully!
✅ Share your app URL (e.g., `your-app.streamlit.app`)
✅ Start testing with your documentation
✅ Generate test cases and scripts

Enjoy your AI-powered QA Agent! 🎉
