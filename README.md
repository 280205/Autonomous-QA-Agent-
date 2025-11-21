# Autonomous QA Agent for Test Case and Script Generation

An intelligent, autonomous QA agent that constructs a "testing brain" from project documentation. The system ingests support documents alongside HTML structure to generate comprehensive test cases and executable Selenium test scripts.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Support Documents](#support-documents)
- [Example Workflow](#example-workflow)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This system provides an end-to-end solution for automated test generation:

1. **Document Ingestion** - Processes product specifications, UI/UX guidelines, API docs, and HTML files
2. **Knowledge Base** - Creates a semantic search-enabled vector database using RAG (Retrieval-Augmented Generation)
3. **Test Case Generation** - AI-powered agent generates structured, documentation-grounded test cases
4. **Script Generation** - Converts test cases into executable Python Selenium scripts

All test reasoning is strictly grounded in the provided documents with no hallucinated features.

## Features

- **Multi-Format Document Support**: .txt, .md, .json, .pdf, .html
- **Vector Database**: ChromaDB with semantic search capabilities
- **Multiple LLM Providers**: OpenAI, Groq, or Ollama
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate test case creation
- **FastAPI Backend**: RESTful API with comprehensive endpoints
- **Streamlit UI**: Intuitive web interface for all operations
- **Test Case Export**: JSON and Markdown formats
- **Script Validation**: Automatic Python syntax validation
- **Documentation Grounding**: All test cases reference source documents

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ChromaDB│ │  LLM Handler │
│(Vector)│ │(OpenAI/Groq) │
└────────┘ └──────────────┘
    │         │
    └────┬────┘
         │
    ┌────┴─────────┐
    │              │
    ▼              ▼
┌──────────┐  ┌────────────┐
│Test Case │  │  Selenium  │
│  Agent   │  │   Agent    │
└──────────┘  └────────────┘
```

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Chrome browser (for running Selenium scripts)
- 4GB+ RAM recommended
- API key for chosen LLM provider (OpenAI or Groq) - Groq is recommended (free tier available)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Ocean.ai
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and add your API keys:

```env
# Choose your LLM provider: openai, groq, or ollama
LLM_PROVIDER=groq

# For Groq (recommended - free tier available)
GROQ_API_KEY=your_groq_api_key_here

# For OpenAI (requires paid account)
OPENAI_API_KEY=your_openai_api_key_here

# For Ollama (local, no API key needed)
OLLAMA_BASE_URL=http://localhost:11434
```

#### Getting API Keys

**Groq (Recommended - Free):**
1. Visit https://console.groq.com/
2. Sign up for free account
3. Generate API key from dashboard
4. Groq offers fast inference with generous free tier

**OpenAI:**
1. Visit https://platform.openai.com/
2. Create account and add payment method
3. Generate API key from API keys page

**Ollama (Local - No API Key):**
1. Install Ollama from https://ollama.ai/
2. Run: `ollama pull llama2`
3. Start Ollama service

## Configuration

The system is configured via environment variables in `.env`:

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `LLM_PROVIDER` | LLM service to use | `groq` | `openai`, `groq`, `ollama` |
| `GROQ_API_KEY` | Groq API key | - | Your API key |
| `OPENAI_API_KEY` | OpenAI API key | - | Your API key |
| `GROQ_MODEL` | Groq model name | `mixtral-8x7b-32768` | Any Groq model |
| `OPENAI_MODEL` | OpenAI model name | `gpt-3.5-turbo` | `gpt-3.5-turbo`, `gpt-4`, etc. |
| `EMBEDDING_MODEL` | Sentence transformer model | `sentence-transformers/all-MiniLM-L6-v2` | Any HF model |
| `CHROMA_DB_PATH` | Vector DB storage path | `./chroma_db` | Any directory path |

## Usage

### Starting the Application

#### 1. Start FastAPI Backend

Open a terminal and run:

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger): `http://localhost:8000/docs`

#### 2. Start Streamlit UI

Open a new terminal and run:

```bash
streamlit run app.py
```

The UI will open in your browser at `http://localhost:8501`

### Using the System

#### Step 1: Upload Documents

1. Navigate to the **Document Upload** page
2. Click "Browse files" and select your support documents:
   - `product_specs.md`
   - `ui_ux_guide.txt`
   - `api_endpoints.json`
   - `checkout.html`
   - `test_scenarios.md` (optional)
3. Click **Upload Documents**
4. Wait for confirmation

#### Step 2: Build Knowledge Base

1. After uploading, click **Build Knowledge Base**
2. The system will:
   - Process all documents
   - Extract and chunk text
   - Generate embeddings
   - Store in vector database
3. Wait for "Knowledge base built successfully" message
4. Check the status in the sidebar (should show green checkmark)

#### Step 3: Generate Test Cases

1. Navigate to **Test Case Generation** page
2. Either select a suggested scenario or write your own query
3. Example queries:
   - "Generate all positive and negative test cases for the discount code feature"
   - "Generate test cases for form validation"
   - "Generate test cases for shopping cart functionality"
4. Click **Generate Test Cases**
5. Wait 30-60 seconds for generation
6. Review generated test cases
7. Export as JSON or Markdown if needed

#### Step 4: Generate Selenium Scripts

1. Navigate to **Script Generation** page
2. (Optional) Upload `checkout.html` for better accuracy
3. Select a test case from the dropdown
4. Click **Generate Selenium Script**
5. Wait 30-60 seconds for generation
6. Review the generated script
7. Download the script as a `.py` file

#### Step 5: Run Selenium Scripts

Save the generated script and run it:

```bash
python test_script.py
```

The script will:
- Launch Chrome browser
- Execute the test steps
- Perform assertions
- Report results
- Close browser

## Project Structure

```
Ocean.ai/
├── backend/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── document_processor.py  # Document parsing
│   ├── vector_db.py           # ChromaDB integration
│   ├── llm_handler.py         # LLM interactions
│   ├── test_case_agent.py     # Test case generation
│   ├── selenium_agent.py      # Script generation
│   └── main.py                # FastAPI application
├── project_assets/
│   ├── checkout.html          # Target web application
│   ├── product_specs.md       # Product specifications
│   ├── ui_ux_guide.txt        # UI/UX guidelines
│   ├── api_endpoints.json     # API documentation
│   └── test_scenarios.md      # Test scenarios (optional)
├── app.py                     # Streamlit UI
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## API Documentation

### Endpoints

#### Health Check
```
GET /health
```
Returns API health status and configuration.

#### Upload Documents
```
POST /upload
Content-Type: multipart/form-data
```
Upload multiple documents for processing.

#### Build Knowledge Base
```
POST /build-knowledge-base?reset=false
```
Process documents and create vector embeddings.

#### Generate Test Cases
```
POST /generate-test-cases
Content-Type: application/json

{
  "query": "Generate test cases for discount code feature",
  "top_k": 5
}
```
Generate structured test cases from documentation.

#### Generate Selenium Script
```
POST /generate-selenium-script
Content-Type: application/json

{
  "test_case": {...},
  "html_content": "optional html content"
}
```
Generate executable Selenium Python script.

#### Get Knowledge Base Stats
```
GET /knowledge-base/stats
```
Returns statistics about uploaded documents and vector database.

#### Get Test Suggestions
```
GET /test-suggestions
```
Returns suggested test scenario queries.

#### Reset Knowledge Base
```
DELETE /knowledge-base/reset
```
Delete all documents and reset vector database.

For interactive API documentation, visit `http://localhost:8000/docs` when the backend is running.

## Support Documents

The system includes comprehensive support documents in `project_assets/`:

### 1. checkout.html
A complete e-commerce checkout page with:
- Product catalog (3 products)
- Shopping cart with quantity management
- Discount code input (SAVE15 for 15% off)
- Customer information form
- Shipping method selection (Standard/Express)
- Payment method selection (Credit Card/PayPal)
- Form validation
- Success message display

### 2. product_specs.md
Detailed product specifications including:
- Product catalog details
- Shopping cart functionality
- Discount code rules (SAVE15 = 15% off)
- Shipping methods (Standard free, Express $10)
- Payment methods
- Form validation requirements
- Business rules and calculations
- Edge cases and error handling

### 3. ui_ux_guide.txt
Comprehensive UI/UX guidelines covering:
- Color scheme (Success green, Error red, Info blue)
- Typography and font sizes
- Layout and spacing rules
- Component design (buttons, forms, cards)
- Interactive behavior (hover effects, transitions)
- Validation and feedback patterns
- Error message styling
- Accessibility guidelines

### 4. api_endpoints.json
Mock API specification with:
- Product listing endpoint
- Cart management endpoints (add, update, remove)
- Discount validation endpoint
- Shipping calculation endpoint
- Order submission endpoint
- Data models and schemas
- Business logic rules
- Error response formats

### 5. test_scenarios.md
Additional test scenarios including:
- Functional test scenarios
- Boundary value tests
- Error handling tests
- UI/UX validation tests
- Integration tests
- Negative test cases
- Cross-browser compatibility
- Performance tests

## Example Workflow

Here's a complete example workflow:

### 1. Start Services

Terminal 1:
```bash
python -m uvicorn backend.main:app --reload
```

Terminal 2:
```bash
streamlit run app.py
```

### 2. Upload Documents

In the Streamlit UI:
1. Go to "Document Upload" page
2. Upload all 4 support documents
3. Click "Build Knowledge Base"
4. Wait for success message

### 3. Generate Test Cases

1. Go to "Test Case Generation" page
2. Enter query: "Generate comprehensive test cases for the discount code SAVE15 feature including positive and negative scenarios"
3. Click "Generate Test Cases"
4. Review generated test cases:
   - TC-001: Valid discount code application
   - TC-002: Invalid discount code
   - TC-003: Empty discount code
   - TC-004: Case insensitive validation
   - etc.

### 4. Generate Script

1. Go to "Script Generation" page
2. Upload `checkout.html`
3. Select test case "TC-001: Valid discount code"
4. Click "Generate Selenium Script"
5. Review generated script
6. Download as `test_discount_valid.py`

### 5. Run Test

```bash
python test_discount_valid.py
```

Expected output:
```
.
----------------------------------------------------------------------
Ran 1 test in 5.234s

OK
```

## Troubleshooting

### Backend Won't Start

**Problem:** `ModuleNotFoundError` when starting backend

**Solution:**
```bash
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

### "Backend API is not running" in Streamlit

**Problem:** Streamlit can't connect to FastAPI

**Solution:**
1. Make sure FastAPI is running: `python -m uvicorn backend.main:app --reload`
2. Check if port 8000 is available
3. Verify in browser: `http://localhost:8000/health`

### "GROQ_API_KEY is required" Error

**Problem:** Missing or invalid API key

**Solution:**
1. Create `.env` file from `.env.example`
2. Add your Groq API key: `GROQ_API_KEY=your_key_here`
3. Restart backend

### No Test Cases Generated

**Problem:** LLM returns empty response

**Solution:**
1. Check if knowledge base is built (sidebar should show green checkmark)
2. Try a more specific query
3. Increase `top_k` parameter to retrieve more context
4. Check backend logs for errors
5. Verify API key is valid

### Selenium Script Fails to Run

**Problem:** `WebDriverException` or import errors

**Solution:**
```bash
# Install required packages
pip install selenium webdriver-manager

# Make sure Chrome is installed
# Update the HTML file path in the script
```

### Vector Database Issues

**Problem:** ChromaDB errors or slow performance

**Solution:**
```bash
# Reset the database
# In Streamlit UI, go to Document Upload
# Click "Rebuild (Reset)"

# Or manually delete:
rm -rf chroma_db/
rm -rf uploaded_docs/
```

### Memory Issues

**Problem:** System runs out of memory

**Solution:**
1. Reduce `CHUNK_SIZE` in config (default: 1000)
2. Reduce `top_k` when generating test cases
3. Process fewer documents at once
4. Use a smaller embedding model

### Import Errors in Generated Scripts

**Problem:** Generated script has import issues

**Solution:**
The scripts should include all necessary imports. If not:

```python
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
```

## Advanced Configuration

### Using Different LLM Models

#### Groq Models
```env
LLM_PROVIDER=groq
GROQ_MODEL=mixtral-8x7b-32768  # Fast and capable
# or
GROQ_MODEL=llama2-70b-4096     # More powerful
```

#### OpenAI Models
```env
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo     # Fast and cost-effective
# or
OPENAI_MODEL=gpt-4             # More powerful
```

#### Ollama (Local)
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
```

### Customizing Chunk Size

Edit `backend/config.py`:

```python
CHUNK_SIZE = 500        # Smaller chunks, more precise
CHUNK_OVERLAP = 100     # Less overlap
```

### Customizing Generation Parameters

Edit `backend/config.py`:

```python
MAX_TOKENS = 3000       # Longer responses
TEMPERATURE = 0.5       # More focused (0.0-1.0)
```

## Performance Optimization

### For Faster Generation

1. Use Groq provider (fastest inference)
2. Reduce `top_k` to 3-5 chunks
3. Use smaller embedding model
4. Keep documents concise

### For Better Quality

1. Use GPT-4 if available
2. Increase `top_k` to 7-10 chunks
3. Provide more detailed documentation
4. Use specific, focused queries

## Security Considerations

1. **API Keys**: Never commit `.env` file to version control
2. **File Uploads**: System validates file extensions and size
3. **Input Validation**: All API endpoints validate input
4. **Sandboxing**: Consider running generated scripts in isolated environment

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or feature requests:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review closed issues on GitHub
3. Open a new issue with details

## Acknowledgments

- Built with FastAPI, Streamlit, LangChain, and ChromaDB
- Uses Sentence Transformers for embeddings
- Supports OpenAI, Groq, and Ollama LLM providers
- Selenium for web automation

## Version History

### v1.0.0 (Current)
- Initial release
- Multi-format document support
- RAG-based test case generation
- Selenium script generation
- FastAPI backend
- Streamlit UI

---

Built with care for automated testing excellence.
