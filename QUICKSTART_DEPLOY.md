# 🎯 Quick Start: Deploy in 5 Minutes

## Backend on Render → Frontend on Streamlit Cloud

---

## 📋 Step 1: Deploy Backend on Render (3 minutes)

1. **Go to**: https://render.com
2. **Sign in** with GitHub
3. **New + → Web Service**
4. **Connect**: `280205/Autonomous-QA-Agent-`
5. **Configure**:
   - Name: `qa-agent-backend`
   - Runtime: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**
6. **Add Environment Variables**:
   ```
   GROQ_API_KEY = your-groq-api-key
   GROQ_MODEL = llama-3.3-70b-versatile
   LLM_PROVIDER = groq
   ```
7. **Click**: Create Web Service
8. **Wait**: 5-10 minutes for deployment
9. **Copy**: Your URL (e.g., `https://qa-agent-backend.onrender.com`)

---

## 🎨 Step 2: Deploy Frontend on Streamlit Cloud (2 minutes)

1. **Go to**: https://share.streamlit.io
2. **Sign in** with GitHub
3. **New app**
4. **Select**:
   - Repository: `280205/Autonomous-QA-Agent-`
   - Branch: `master`
   - Main file: `app.py`
5. **Advanced settings → Secrets**:
   ```toml
   BACKEND_URL = "https://your-backend-url.onrender.com"
   ```
6. **Click**: Deploy!
7. **Wait**: 2-3 minutes

---

## ✅ Step 3: Test Your App

1. Open your Streamlit app URL
2. Upload a document
3. Build knowledge base
4. Generate test cases
5. Generate scripts

**Done! 🎉**

---

## 🔧 Troubleshooting

### Backend not responding?
- Wait 30-60 seconds (cold start on free tier)
- Check Render logs for errors
- Verify environment variables are set

### Frontend can't connect?
- Verify `BACKEND_URL` in Streamlit secrets
- Check CORS is enabled in backend
- Test backend health: `https://your-url.onrender.com/health`

### Knowledge base not building?
- Ensure Groq API key is valid
- Check backend logs for errors
- Verify model name is correct

---

## 📞 Need Help?

**Full Documentation:**
- Backend: `RENDER_DEPLOYMENT.md`
- Frontend: `README_DEPLOYMENT.md`
- General: `README.md`

**Support:**
- Render: https://community.render.com
- Streamlit: https://discuss.streamlit.io

---

## 💡 Pro Tips

1. **Keep Backend Warm**: 
   - Use a service like UptimeRobot (free)
   - Ping your backend every 14 minutes

2. **Custom Domain**:
   - Upgrade Render to $7/month
   - Add your domain in settings

3. **Persistent Storage**:
   - Use Render's persistent disk
   - Or external vector DB (Pinecone)

---

**Your Apps:**
- Backend: `https://qa-agent-backend.onrender.com`
- Frontend: `https://your-app.streamlit.app`

**Total Cost: $0/month** 🎉
