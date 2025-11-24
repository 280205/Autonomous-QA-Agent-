# 🚀 Complete Deployment Guide - Backend + Frontend

## Quick Start (3 Minutes to Deploy!)

Your app is **already optimized** and ready to deploy! 

---

## ⭐ OPTION 1: Streamlit Cloud (All-in-One) - EASIEST

Deploy both backend and frontend together on Streamlit Cloud (100% free).

### Prerequisites
- ✅ GitHub account
- ✅ OpenAI API key ([Get here](https://platform.openai.com/api-keys))

### 🚀 Deploy Now (4 Steps)

#### **STEP 1**: Go to Streamlit Cloud
```
https://share.streamlit.io/
```
Sign in with your GitHub account.

#### **STEP 2**: Create New App
Click **"New app"** button and fill:
- **Repository**: `280205/Autonomous-QA-Agent-`
- **Branch**: `master`
- **Main file path**: `streamlit_app.py` ⚠️ (Important!)

#### **STEP 3**: Advanced Settings
Click **"Advanced settings"** and configure:

**Python version**: 
```
3.11
```

**Secrets** (paste in the text box):
```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
```
Replace `sk-your-actual-key-here` with your real OpenAI API key.

#### **STEP 4**: Deploy!
Click **"Deploy!"** button and wait 3-5 minutes.

Your app will be live at: `https://your-app-name.streamlit.app`

---

## 🎯 OPTION 2: Separate Deployment (Advanced)

Deploy backend on Railway and frontend on Streamlit Cloud.

### A. Deploy Backend on Railway

#### **STEP 1**: Install Railway CLI
```bash
npm install -g @railway/cli
```

Or use Railway web interface (easier):
```
https://railway.app/
```

#### **STEP 2**: Create New Project
1. Sign up/login to Railway
2. Click **"New Project"**
3. Choose **"Deploy from GitHub repo"**
4. Select: `280205/Autonomous-QA-Agent-`

#### **STEP 3**: Configure Backend Service
In Railway dashboard:

**Root Directory**: (leave empty)

**Start Command**:
```bash
cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables**:
```
OPENAI_API_KEY=sk-your-actual-key-here
PORT=8000
```

**Generate Domain**: Click "Generate Domain" to get your backend URL
Example: `https://autonomous-qa-agent-production.up.railway.app`

#### **STEP 4**: Wait for Deployment
Build takes ~2-3 minutes. You'll get a public URL.

### B. Deploy Frontend on Streamlit Cloud

#### **STEP 1**: Go to Streamlit Cloud
```
https://share.streamlit.io/
```

#### **STEP 2**: Create New App
- **Repository**: `280205/Autonomous-QA-Agent-`
- **Branch**: `master`  
- **Main file path**: `app.py` (not streamlit_app.py)

#### **STEP 3**: Advanced Settings

**Python version**: `3.11`

**Secrets**:
```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
BACKEND_URL = "https://your-railway-backend-url.railway.app"
```
Replace the URL with your actual Railway backend URL from Step A.

#### **STEP 4**: Deploy!
Click "Deploy!" and wait 2-3 minutes.

---

## 🔧 Environment Variables Needed

### For All-in-One Deployment (Option 1):
```toml
OPENAI_API_KEY = "sk-..."
```

### For Separate Deployment (Option 2):

**Backend (Railway)**:
```
OPENAI_API_KEY=sk-...
PORT=8000
```

**Frontend (Streamlit)**:
```toml
OPENAI_API_KEY = "sk-..."
BACKEND_URL = "https://your-backend-url.railway.app"
```

---

## 📊 Build Size & Time

**Package Size**: ~50-80MB ✅
**Build Time**: 2-3 minutes ✅
**Deploy Time**: 3-5 minutes total ✅

All optimized for free tier!

---

## ✅ Verification Steps

After deployment, test these features:

1. **Home Page**: Should load with animated UI
2. **Document Upload**: Upload a test PDF/TXT file
3. **Build KB**: Click "Build Knowledge Base"
4. **Generate Test Cases**: Enter a query and generate
5. **Generate Script**: Select test case and generate Selenium script
6. **Dashboard**: Check stats are displaying

---

## 🐛 Troubleshooting

### Error: "Module not found: sentence_transformers"
**Solution**: Files already updated! Just redeploy.

### Error: "Build exceeded limits"
**Solution**: You're using correct requirements.txt already (50MB).

### Error: "OpenAI API key not found"
**Solution**: Add your API key in Streamlit secrets (Step 3).

### Error: "Backend not connecting" (Option 2 only)
**Solution**: 
1. Verify Railway backend is running (check logs)
2. Check `BACKEND_URL` in Streamlit secrets matches Railway URL
3. Ensure Railway backend has public domain generated

### Error: "Port already in use"
**Solution**: For local testing, kill existing processes:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Then restart
python -m uvicorn backend.main:app --reload
```

---

## 💰 Cost Breakdown

### Option 1 (All-in-One):
- **Streamlit Cloud**: FREE (1GB RAM, 1 CPU)
- **OpenAI API**: ~$1-5/month (pay-as-you-go)
- **Total**: ~$1-5/month

### Option 2 (Separate):
- **Railway**: FREE $5 credit/month (enough for small usage)
- **Streamlit Cloud**: FREE
- **OpenAI API**: ~$1-5/month
- **Total**: ~$1-5/month (within Railway free credit)

---

## 🎯 Recommended Approach

**For Solo Use / Testing**: Option 1 (All-in-One)
- Simpler setup
- One deployment
- Perfect for free tier

**For Team / Production**: Option 2 (Separate)
- Better scalability
- Independent backend updates
- Better for high traffic

---

## 📱 Access Your App

After deployment:

**Streamlit Cloud URL Pattern**:
```
https://[username]-autonomous-qa-agent.streamlit.app
or
https://autonomous-qa-agent-[random].streamlit.app
```

**Railway Backend URL Pattern** (if using Option 2):
```
https://[project-name]-production.up.railway.app
```

---

## 🔄 Update Deployed App

To push updates:

```bash
# Make your changes to code
git add .
git commit -m "Your update message"
git push origin master
```

Streamlit Cloud auto-redeploys on git push! 🎉

---

## 📚 Files Overview

**For Deployment**:
- ✅ `streamlit_app.py` - Combined backend+frontend launcher
- ✅ `app.py` - Frontend only (for separate deployment)
- ✅ `backend/main.py` - Backend API
- ✅ `requirements.txt` - Optimized dependencies (50MB)
- ✅ `.streamlit/config.toml` - Streamlit configuration

**Documentation**:
- 📖 `DEPLOY_COMPLETE.md` - This file
- 📖 `DEPLOYMENT_STREAMLIT.md` - Detailed Streamlit guide
- 📖 `CHANGES.md` - What we optimized

---

## 🚀 Ready to Deploy!

Choose your option:

**Quick & Easy**: [Option 1 - All-in-One](#-option-1-streamlit-cloud-all-in-one---easiest)
**Full Control**: [Option 2 - Separate Deployment](#-option-2-separate-deployment-advanced)

---

## 💡 Pro Tips

1. **Use Option 1** for your first deployment (easier)
2. **Get OpenAI API key** before starting
3. **Watch the logs** during first deployment to catch any issues
4. **Test locally first** if unsure: `streamlit run streamlit_app.py`
5. **Share your app** once deployed - it's production-ready!

---

## ❓ Need Help?

1. Check Streamlit logs: App → Manage app → Logs
2. Check Railway logs: Project → Deployments → Logs
3. Verify API keys are correct
4. Try redeploying if first attempt fails

---

## 🎉 That's It!

Your QA Agent is optimized and ready. Follow the steps above and you'll have a live app in 5 minutes!

**Happy Testing!** 🚀
