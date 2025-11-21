# 🚀 Deploy Backend on Render.com

Complete guide to deploy the FastAPI backend on Render's free tier.

---

## Prerequisites

- ✅ GitHub repository (already pushed!)
- ✅ Render account (free at https://render.com)
- ✅ Your Groq API key

---

## 🔧 Step-by-Step Deployment

### 1. Sign Up / Sign In to Render

1. Go to https://render.com
2. Click "Get Started" or "Sign In"
3. Choose "Sign in with GitHub"
4. Authorize Render to access your repositories

---

### 2. Create New Web Service

1. From the Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Build and deploy from a Git repository"**
4. Click **"Connect account"** if needed, then find your repository:
   - Repository: `280205/Autonomous-QA-Agent-`
5. Click **"Connect"**

---

### 3. Configure Your Service

Fill in the following settings:

#### Basic Settings
- **Name**: `qa-agent-backend` (or any name you prefer)
- **Region**: Choose closest to you (Oregon, Frankfurt, Singapore, etc.)
- **Branch**: `master`
- **Root Directory**: Leave empty (or `.` for root)
- **Runtime**: `Python 3`

#### Build & Deploy Settings
- **Build Command**:
  ```bash
  pip install -r requirements.txt
  ```

- **Start Command**:
  ```bash
  python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```

#### Instance Settings
- **Plan**: Select **"Free"** ($0/month)
  - 512 MB RAM
  - Spins down after 15 min of inactivity
  - Spins up automatically on request

---

### 4. Add Environment Variables

Scroll down to **"Environment Variables"** section and add:

| Key | Value |
|-----|-------|
| `GROQ_API_KEY` | `your-groq-api-key-here` |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` |
| `LLM_PROVIDER` | `groq` |
| `PYTHON_VERSION` | `3.11.0` |

⚠️ **Important:** Replace `your-groq-api-key-here` with your actual Groq API key!

---

### 5. Deploy!

1. Click **"Create Web Service"** button at the bottom
2. Wait for deployment (5-10 minutes first time)
3. Watch the build logs for any errors
4. Once deployed, you'll see: ✅ **"Live"** status

---

### 6. Get Your Backend URL

After deployment completes:
- Your backend URL will be: `https://qa-agent-backend.onrender.com`
- Or similar based on your service name
- Copy this URL - you'll need it for the frontend!

---

## 🧪 Test Your Backend

Test if it's working:

```bash
curl https://your-backend-url.onrender.com/health
```

Should return:
```json
{"status": "healthy"}
```

---

## 🔗 Connect Frontend to Backend

### Option A: Update app.py Locally

1. Open `app.py`
2. Find line ~15 and update:
   ```python
   API_BASE_URL = os.getenv("BACKEND_URL", "https://your-backend-url.onrender.com")
   ```
3. Commit and push:
   ```bash
   git add app.py
   git commit -m "Update backend URL for Render deployment"
   git push
   ```

### Option B: Use Streamlit Secrets (Recommended)

When deploying to Streamlit Cloud, add to secrets:
```toml
BACKEND_URL = "https://your-backend-url.onrender.com"
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- **Spin Down**: Service sleeps after 15 min of inactivity
- **Cold Start**: First request after sleep takes 30-60 seconds
- **Monthly Limit**: 750 hours/month (enough for development)

### Persistence Issues
- **ChromaDB**: Will reset on each deployment
- **Uploaded Files**: Not persistent across deployments
- **Solution**: Use external storage (S3, Pinecone) for production

### Performance Tips
- Keep the service "warm" by pinging every 14 minutes
- Upgrade to paid plan ($7/month) to avoid spin-down
- Use persistent disks for ChromaDB storage

---

## 🐛 Troubleshooting

### Build Fails
- Check Python version compatibility
- Verify `requirements.txt` is complete
- Check build logs for missing dependencies

### Deploy Fails
- Verify start command is correct
- Check environment variables are set
- Look for port binding issues in logs

### Service Crashes
- Check logs in Render dashboard
- Verify Groq API key is valid
- Check for missing dependencies

### CORS Issues
If frontend can't connect to backend:
1. Open `backend/main.py`
2. Verify CORS is configured:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Or specific Streamlit URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

---

## 📊 Monitor Your Service

In Render Dashboard:
- **Logs**: View real-time application logs
- **Metrics**: CPU, Memory usage
- **Events**: Deployment history
- **Settings**: Update environment variables

---

## 🎯 Next Steps

After backend is deployed:

1. ✅ Copy your backend URL
2. ✅ Update frontend configuration
3. ✅ Deploy frontend on Streamlit Cloud
4. ✅ Test the full application
5. ✅ Share your deployed app!

---

## 💰 Cost Estimate

**Free Tier:**
- Backend on Render: $0/month
- Frontend on Streamlit Cloud: $0/month
- **Total: FREE! 🎉**

**Paid Tier (Optional):**
- Render Standard: $7/month (no spin-down)
- Custom domain: Free with paid plan
- Persistent storage: $0.25/GB/month

---

## 🔐 Security Best Practices

1. ✅ Keep API keys in environment variables (never in code)
2. ✅ Use `.gitignore` to exclude `.env` files
3. ✅ Rotate API keys periodically
4. ✅ Enable HTTPS only (default on Render)
5. ✅ Add authentication for production use

---

## 📞 Support

**Render Documentation:**
- https://render.com/docs

**Need Help?**
- Render Community: https://community.render.com
- Discord: https://discord.gg/render

---

## ✅ Deployment Checklist

- [ ] Render account created
- [ ] Repository connected
- [ ] Service configured (Python 3, free tier)
- [ ] Build command set
- [ ] Start command set
- [ ] Environment variables added
- [ ] Service deployed successfully
- [ ] Backend URL copied
- [ ] Health endpoint tested
- [ ] Frontend connected
- [ ] Full app tested

---

**Your backend will be live at:**
`https://qa-agent-backend.onrender.com`

Good luck! 🚀
