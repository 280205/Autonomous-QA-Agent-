"""
FastAPI Backend for the QA Agent System.
Provides endpoints for document ingestion, test case generation, and script generation.
"""

import os
import shutil
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.config import Config
from backend.document_processor import DocumentProcessor
from backend.vector_db import VectorDatabase
from backend.llm_handler import LLMHandler
from backend.test_case_agent import TestCaseAgent
from backend.selenium_agent import SeleniumScriptAgent


# Initialize FastAPI app
app = FastAPI(
    title="QA Agent API",
    description="Autonomous QA Agent for Test Case and Script Generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
vector_db = VectorDatabase()
llm_handler = LLMHandler()
test_case_agent = TestCaseAgent(vector_db, llm_handler)
selenium_agent = SeleniumScriptAgent(vector_db, llm_handler)

# Pydantic models
class TestCaseRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class ScriptGenerationRequest(BaseModel):
    test_case: dict
    html_content: Optional[str] = None


class StatusResponse(BaseModel):
    status: str
    message: str
    details: Optional[dict] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "QA Agent API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "upload": "/upload",
            "build_kb": "/build-knowledge-base",
            "generate_tests": "/generate-test-cases",
            "generate_script": "/generate-selenium-script",
            "suggestions": "/test-suggestions",
            "stats": "/knowledge-base/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Validate configuration
        Config.validate_config()
        
        # Check vector DB
        stats = vector_db.get_collection_stats()
        
        return {
            "status": "healthy",
            "llm_provider": Config.LLM_PROVIDER,
            "vector_db": {
                "connected": True,
                "documents": stats.get("count", 0)
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload support documents.
    Accepts: .txt, .md, .json, .pdf, .html files
    """
    try:
        uploaded_files = []
        
        for file in files:
            # Validate file extension
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in Config.ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {file_ext}. Allowed: {Config.ALLOWED_EXTENSIONS}"
                )
            
            # Save file
            file_path = os.path.join(Config.UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                if len(content) > Config.MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"File {file.filename} exceeds maximum size of {Config.MAX_FILE_SIZE} bytes"
                    )
                f.write(content)
            
            uploaded_files.append({
                "filename": file.filename,
                "path": file_path,
                "size": len(content)
            })
        
        return StatusResponse(
            status="success",
            message=f"Successfully uploaded {len(uploaded_files)} file(s)",
            details={"files": uploaded_files}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/build-knowledge-base")
async def build_knowledge_base(reset: bool = False):
    """
    Build knowledge base from uploaded documents.
    Processes all files in the upload directory and creates vector embeddings.
    """
    try:
        # Check if documents exist
        if not os.path.exists(Config.UPLOAD_DIR):
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded. Please upload documents first."
            )
        
        uploaded_files = [
            f for f in os.listdir(Config.UPLOAD_DIR)
            if Path(f).suffix.lower() in Config.ALLOWED_EXTENSIONS
        ]
        
        if not uploaded_files:
            raise HTTPException(
                status_code=400,
                detail="No valid documents found in upload directory."
            )
        
        # Create or reset collection
        vector_db.create_collection(reset=reset)
        
        # Process and add documents
        documents = []
        for filename in uploaded_files:
            file_path = os.path.join(Config.UPLOAD_DIR, filename)
            try:
                doc = DocumentProcessor.process_file(file_path)
                documents.append(doc)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        
        if not documents:
            raise HTTPException(
                status_code=500,
                detail="Failed to process any documents"
            )
        
        # Add to vector database
        num_chunks = vector_db.add_documents(documents)
        
        return StatusResponse(
            status="success",
            message="Knowledge base built successfully",
            details={
                "files_processed": len(documents),
                "chunks_created": num_chunks,
                "files": [doc["source"] for doc in documents]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-test-cases")
async def generate_test_cases(request: TestCaseRequest):
    """
    Generate test cases based on user query.
    Uses RAG to retrieve relevant documentation and LLM to generate structured test cases.
    """
    try:
        # Check if knowledge base exists
        stats = vector_db.get_collection_stats()
        if not stats.get("exists") or stats.get("count", 0) == 0:
            raise HTTPException(
                status_code=400,
                detail="Knowledge base is empty. Please build the knowledge base first."
            )
        
        # Generate test cases
        test_cases = test_case_agent.generate_test_cases(
            query=request.query,
            top_k=request.top_k
        )
        
        return {
            "status": "success",
            "query": request.query,
            "test_cases": test_cases,
            "count": len(test_cases)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-selenium-script")
async def generate_selenium_script(request: ScriptGenerationRequest):
    """
    Generate Selenium Python script from test case.
    Uses test case details and HTML structure to create executable script.
    """
    try:
        # Check if knowledge base exists
        stats = vector_db.get_collection_stats()
        if not stats.get("exists") or stats.get("count", 0) == 0:
            raise HTTPException(
                status_code=400,
                detail="Knowledge base is empty. Please build the knowledge base first."
            )
        
        # Generate script
        script = selenium_agent.generate_selenium_script(
            test_case=request.test_case,
            html_content=request.html_content
        )
        
        # Validate syntax
        validation = selenium_agent.validate_script_syntax(script)
        
        return {
            "status": "success",
            "test_id": request.test_case.get("test_id", "unknown"),
            "script": script,
            "validation": validation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test-suggestions")
async def get_test_suggestions():
    """
    Get suggested test scenarios based on uploaded documentation.
    """
    try:
        suggestions = test_case_agent.suggest_test_scenarios()
        
        return {
            "status": "success",
            "suggestions": suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge-base/stats")
async def get_knowledge_base_stats():
    """
    Get statistics about the knowledge base.
    """
    try:
        stats = vector_db.get_collection_stats()
        
        # Get uploaded files
        uploaded_files = []
        if os.path.exists(Config.UPLOAD_DIR):
            uploaded_files = [
                f for f in os.listdir(Config.UPLOAD_DIR)
                if Path(f).suffix.lower() in Config.ALLOWED_EXTENSIONS
            ]
        
        return {
            "status": "success",
            "vector_db": stats,
            "uploaded_files": uploaded_files,
            "upload_directory": Config.UPLOAD_DIR
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/knowledge-base/reset")
async def reset_knowledge_base():
    """
    Reset the knowledge base and delete all uploaded documents.
    """
    try:
        # Delete vector database
        vector_db.delete_collection()
        
        # Delete uploaded files
        if os.path.exists(Config.UPLOAD_DIR):
            shutil.rmtree(Config.UPLOAD_DIR)
            os.makedirs(Config.UPLOAD_DIR)
        
        return StatusResponse(
            status="success",
            message="Knowledge base and uploaded documents have been reset"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=Config.BACKEND_HOST,
        port=Config.BACKEND_PORT,
        reload=True
    )
