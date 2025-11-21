# Quick Setup Guide

Get the QA Agent system up and running in 5 minutes.

## 1. Prerequisites Check

```bash
# Check Python version (needs 3.9+)
python --version

# Check pip
pip --version

# Check Chrome browser
# Make sure Chrome is installed
```

## 2. Setup Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will take 2-3 minutes.

## 4. Get API Key (Choose One)

### Option A: Groq (Recommended - Free & Fast)

1. Visit: https://console.groq.com/
2. Sign up (free)
3. Go to "API Keys"
4. Click "Create API Key"
5. Copy the key

### Option B: OpenAI (Paid)

1. Visit: https://platform.openai.com/
2. Sign up and add payment
3. Go to API Keys
4. Create new key
5. Copy the key

### Option C: Ollama (Local - No Key Needed)

```bash
# Install Ollama from https://ollama.ai/
ollama pull llama2
ollama serve
```

## 5. Configure Environment

```bash
# Copy example env file
copy .env.example .env    # Windows
# or
cp .env.example .env      # Linux/Mac
```

Edit `.env` and add your API key:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_actual_api_key_here
```

## 6. Start the System

### Option A: Using Startup Scripts

**Windows:**
```cmd
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - UI:**
```bash
streamlit run app.py
```

## 7. Access the Application

- **Streamlit UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 8. Quick Test

1. Open Streamlit UI (http://localhost:8501)
2. Go to "Document Upload"
3. Upload files from `project_assets/` folder
4. Click "Build Knowledge Base"
5. Wait for success
6. Go to "Test Case Generation"
7. Enter query: "Generate test cases for discount code"
8. Click "Generate Test Cases"
9. View results!

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --force-reinstall
```

### "Backend not running" in UI
Make sure FastAPI is running on port 8000:
```bash
python -m uvicorn backend.main:app --reload
```

### "GROQ_API_KEY required" error
1. Check `.env` file exists
2. Verify API key is correct
3. Restart the backend

### Port already in use
```bash
# Change port in command
python -m uvicorn backend.main:app --reload --port 8001

# Update API_BASE_URL in app.py:
# API_BASE_URL = "http://localhost:8001"
```

### Slow generation
- Use Groq provider (fastest)
- Reduce top_k parameter
- Use smaller embedding model

## First Time Usage

1. **Upload Documents** (2-3 minutes)
   - Upload all files from `project_assets/`
   - Click "Build Knowledge Base"
   - Wait for completion

2. **Generate Test Cases** (1-2 minutes)
   - Go to Test Case Generation
   - Try: "Generate all test cases for form validation"
   - Review results

3. **Generate Script** (1-2 minutes)
   - Go to Script Generation
   - Upload checkout.html
   - Select a test case
   - Generate script
   - Download and run

## System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Internet connection for API calls
- **Browser**: Chrome, Firefox, Edge, or Safari

## File Locations

```
Ocean.ai/
├── backend/          # API and agents
├── project_assets/   # Sample documents
├── chroma_db/        # Vector database (auto-created)
├── uploaded_docs/    # Uploaded files (auto-created)
├── app.py            # Streamlit UI
└── .env              # Your configuration
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [DEMO_GUIDE.md](DEMO_GUIDE.md) for creating demo video
- Review [example_test_script.py](example_test_script.py) for script examples
- Explore the API at http://localhost:8000/docs

## Common Commands

```bash
# Start backend
python -m uvicorn backend.main:app --reload

# Start UI
streamlit run app.py

# Run example test
python example_test_script.py

# Check API health
curl http://localhost:8000/health

# Install new package
pip install package_name
pip freeze > requirements.txt
```

## Getting Help

1. Check the [Troubleshooting section in README.md](README.md#troubleshooting)
2. Review API documentation at http://localhost:8000/docs
3. Check backend logs in the terminal
4. Verify all files in `project_assets/` folder

## Configuration Options

### Switch LLM Provider

Edit `.env`:

```env
# Use Groq (free, fast)
LLM_PROVIDER=groq
GROQ_API_KEY=your_key

# Use OpenAI (paid, powerful)
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key

# Use Ollama (local, free)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
```

### Adjust Generation Quality

Edit `backend/config.py`:

```python
CHUNK_SIZE = 1000       # Increase for more context
TOP_K_RESULTS = 5       # Increase for more context
TEMPERATURE = 0.7       # Lower for more focused output
MAX_TOKENS = 2000       # Increase for longer output
```

---

That's it! You should now have a working QA Agent system.

For detailed information, see [README.md](README.md).
