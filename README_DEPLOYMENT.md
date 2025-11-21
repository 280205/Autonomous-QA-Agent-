# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub account with your repository
- Streamlit Cloud account (free at https://share.streamlit.io)
- Groq API key

## Deployment Steps

### 1. Prepare Your Repository
✅ Already done! Your code is pushed to:
```
https://github.com/280205/Autonomous-QA-Agent-.git
```

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository: `280205/Autonomous-QA-Agent-`
   - Branch: `master`
   - Main file path: `app.py`

3. **Configure Secrets**
   - Click "Advanced settings"
   - Go to "Secrets" section
   - Add your environment variables:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   GROQ_MODEL = "llama-3.3-70b-versatile"
   LLM_PROVIDER = "groq"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-5 minutes for deployment

### 3. Important Notes

⚠️ **Backend Service Required**
- The FastAPI backend needs to be hosted separately
- Options:
  - Railway.app (free tier)
  - Render.com (free tier)
  - Heroku (paid)
  - AWS/Azure/GCP

⚠️ **Update Backend URL in app.py**
Once backend is deployed, update line ~13 in `app.py`:
```python
API_URL = "https://your-backend-url.com"  # Change from localhost:8000
```

### 4. Alternative: Full Deployment

For a complete deployment including backend:

#### Deploy Backend on Railway
1. Go to https://railway.app
2. Connect GitHub repository
3. Select `backend` directory
4. Add environment variables in Railway dashboard
5. Deploy and get backend URL

#### Deploy Frontend on Streamlit Cloud
1. Update `API_URL` in app.py with Railway backend URL
2. Commit and push changes
3. Deploy on Streamlit Cloud as described above

## Limitations on Streamlit Cloud

- **No FastAPI backend** - Streamlit Cloud only runs Streamlit apps
- **ChromaDB storage** - Resets on each deployment (use external vector DB for production)
- **File uploads** - Limited to session storage
- **Selenium** - May have issues with browser automation

## Production Recommendations

For a production-ready deployment:
1. Host backend on Railway/Render/AWS
2. Use persistent vector database (Pinecone, Weaviate, Qdrant)
3. Add authentication
4. Use external storage for uploaded documents (S3, Azure Blob)
5. Implement proper error handling and logging

## Testing Deployment

Once deployed, test:
1. ✅ Document upload works
2. ✅ Knowledge base builds successfully
3. ✅ Test cases generate properly
4. ✅ Scripts export correctly
5. ✅ All pages accessible

## Support

If you encounter issues:
- Check Streamlit Cloud logs
- Verify secrets are set correctly
- Ensure backend is running and accessible
- Check API URL configuration

---

**Your App URL will be:**
`https://autonomous-qa-agent.streamlit.app`
(or similar based on availability)
