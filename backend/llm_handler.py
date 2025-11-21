"""
LLM handler for interacting with different LLM providers (OpenAI, Groq, Ollama).
"""

from typing import List, Dict, Any, Optional
import openai
from backend.config import Config


class LLMHandler:
    """Handle LLM interactions for test case and script generation"""
    
    def __init__(self):
        """Initialize LLM handler based on configuration"""
        self.config = Config.get_llm_config()
        self.provider = self.config["provider"]
        
        if self.provider == "openai":
            openai.api_key = self.config["api_key"]
            self.model = self.config["model"]
            self.client = openai.OpenAI(api_key=self.config["api_key"])
        elif self.provider == "groq":
            self.model = self.config["model"]
            self.client = openai.OpenAI(
                api_key=self.config["api_key"],
                base_url="https://api.groq.com/openai/v1"
            )
        elif self.provider == "ollama":
            self.model = self.config["model"]
            self.client = openai.OpenAI(
                api_key="ollama",  # Ollama doesn't require API key
                base_url=f"{self.config['base_url']}/v1"
            )
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        temperature = temperature or Config.TEMPERATURE
        max_tokens = max_tokens or Config.MAX_TOKENS
        
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating text with {self.provider}: {str(e)}")
    
    def generate_with_context(
        self,
        query: str,
        context_chunks: List[Dict[str, Any]],
        system_prompt: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Generate text with RAG context.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Generated text
        """
        # Format context
        context_text = self._format_context(context_chunks)
        
        # Create prompt with context
        full_prompt = f"""Context from documentation:

{context_text}

---

User Query: {query}

Based STRICTLY on the provided context above, generate your response. Do not include any information that is not explicitly mentioned in the context."""
        
        return self.generate(
            prompt=full_prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
    
    def _format_context(self, context_chunks: List[Dict[str, Any]]) -> str:
        """Format context chunks into a readable string"""
        formatted_chunks = []
        
        for i, chunk in enumerate(context_chunks, 1):
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})
            source = metadata.get("source", "unknown")
            
            formatted_chunks.append(f"""Source: {source}
Content:
{content}
""")
        
        return "\n---\n".join(formatted_chunks)
