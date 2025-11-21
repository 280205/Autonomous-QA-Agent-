"""
Configuration module for the QA Agent system.
Handles environment variables and application settings.
"""

import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "groq", "ollama"] = os.getenv("LLM_PROVIDER", "groq")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Model Names
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Embedding Model
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Vector Database
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
    # Server Configuration
    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    
    # File Upload Settings
    UPLOAD_DIR: str = "./uploaded_docs"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".txt", ".md", ".json", ".pdf", ".html", ".htm"}
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 5
    
    # Generation Settings
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration based on provider"""
        if cls.LLM_PROVIDER == "openai":
            return {
                "provider": "openai",
                "api_key": cls.OPENAI_API_KEY,
                "model": cls.OPENAI_MODEL
            }
        elif cls.LLM_PROVIDER == "groq":
            return {
                "provider": "groq",
                "api_key": cls.GROQ_API_KEY,
                "model": cls.GROQ_MODEL
            }
        elif cls.LLM_PROVIDER == "ollama":
            return {
                "provider": "ollama",
                "base_url": cls.OLLAMA_BASE_URL,
                "model": cls.OLLAMA_MODEL
            }
        else:
            raise ValueError(f"Unsupported LLM provider: {cls.LLM_PROVIDER}")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration based on selected provider"""
        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        elif cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required when using Groq provider")
        return True


# Create upload directory if it doesn't exist
os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
