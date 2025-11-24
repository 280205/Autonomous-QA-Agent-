"""
Simple text-based search database - no embeddings, no downloads!
Uses basic keyword matching for instant startup.
"""

import os
import re
from typing import List, Dict, Any, Optional
from collections import defaultdict
from backend.config import Config
from backend.document_processor import DocumentProcessor


class VectorDatabase:
    """Simple text search database - no embeddings needed!"""
    
    def __init__(self, persist_directory: str = None):
        """Initialize simple text search database."""
        self.persist_directory = persist_directory or Config.CHROMA_DB_PATH
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # In-memory storage - simple and fast!
        self.documents = []  # List of {id, text, metadata}
        self.collection_name = "qa_documents"
        self.collection = self
        
        print("VectorDatabase initialized (instant, no downloads needed)!")
    
    def create_collection(self, reset: bool = False) -> None:
        """Create or reset collection."""
        if reset:
            self.documents = []
        self.collection = self
    
    def add_documents(
        self,
        documents: List[Dict[str, Any]],
        chunk_size: int = None,
        chunk_overlap: int = None
    ) -> int:
        """
        Add documents to the vector database.
        
        Args:
            documents: List of documents with 'content' and 'metadata' keys
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            Number of chunks added
        """
        if not self.collection:
            self.create_collection()
        
        chunk_size = chunk_size or Config.CHUNK_SIZE
        chunk_overlap = chunk_overlap or Config.CHUNK_OVERLAP
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        chunk_counter = 0
        
        for doc in documents:
            content = doc["content"]
            metadata = doc.get("metadata", {})
            source = doc.get("source", "unknown")
            
            # Chunk the document
            chunks = DocumentProcessor.chunk_text(content, chunk_size, chunk_overlap)
            
            for i, chunk in enumerate(chunks):
                if chunk.strip():  # Only add non-empty chunks
                    chunk_id = f"{source}_chunk_{i}_{chunk_counter}"
                    
                    all_chunks.append(chunk)
                    all_metadatas.append({
                        **metadata,
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    })
                    all_ids.append(chunk_id)
                    
                    chunk_counter += 1
        
        if all_chunks:
            # Store in memory
            for i, chunk in enumerate(all_chunks):
                self.documents.append({
                    'id': all_ids[i],
                    'text': chunk,
                    'metadata': all_metadatas[i]
                })
        
        return len(all_chunks)
    
    def search(
        self,
        query: str,
        top_k: int = None,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Metadata filters
            
        Returns:
            List of relevant documents with metadata
        """
        if not self.collection:
            self.create_collection()
        
        top_k = top_k or Config.TOP_K_RESULTS
        
        # Simple keyword-based search - instant and effective!
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        # Score documents by keyword overlap
        scored_docs = []
        for doc in self.documents:
            text_lower = doc['text'].lower()
            text_words = set(re.findall(r'\w+', text_lower))
            
            # Calculate overlap score
            overlap = len(query_words & text_words)
            if overlap > 0:
                scored_docs.append({
                    'content': doc['text'],
                    'metadata': doc['metadata'],
                    'score': overlap,
                    'distance': 1.0 / (1.0 + overlap)  # Lower is better
                })
        
        # Sort by score (higher is better) and return top_k
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:top_k]
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents"""
        return [{'id': doc['id'], 'content': doc['text'], 'metadata': doc['metadata']} 
                for doc in self.documents]
    
    def delete_collection(self) -> None:
        """Delete the collection"""
        self.documents = []
        self.collection = None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        return {
            "exists": len(self.documents) > 0,
            "count": len(self.documents),
            "name": self.collection_name
        }
