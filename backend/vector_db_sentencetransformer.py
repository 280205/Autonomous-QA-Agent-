"""
Vector database management using ChromaDB for semantic search and retrieval.
"""

import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from backend.config import Config
from backend.document_processor import DocumentProcessor


class VectorDatabase:
    """Manage vector database operations for document storage and retrieval"""
    
    def __init__(self, persist_directory: str = None):
        """
        Initialize vector database.
        
        Args:
            persist_directory: Directory to persist the database
        """
        self.persist_directory = persist_directory or Config.CHROMA_DB_PATH
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
        
        # Collection name
        self.collection_name = "qa_documents"
        self.collection = None
    
    def create_collection(self, reset: bool = False) -> None:
        """
        Create or get collection.
        
        Args:
            reset: If True, delete existing collection and create new one
        """
        if reset:
            try:
                self.client.delete_collection(self.collection_name)
            except:
                pass
        
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "QA Agent document collection"}
            )
    
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
            # Generate embeddings
            embeddings = self.embedding_model.encode(
                all_chunks,
                convert_to_numpy=True,
                show_progress_bar=True
            ).tolist()
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=all_chunks,
                metadatas=all_metadatas,
                ids=all_ids
            )
        
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
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True
        ).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        
        if results and results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return formatted_results
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from the collection"""
        if not self.collection:
            return []
        
        results = self.collection.get()
        
        formatted_results = []
        if results and results['documents']:
            for i in range(len(results['documents'])):
                formatted_results.append({
                    "id": results['ids'][i],
                    "content": results['documents'][i],
                    "metadata": results['metadatas'][i] if results['metadatas'] else {}
                })
        
        return formatted_results
    
    def delete_collection(self) -> None:
        """Delete the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = None
        except:
            pass
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        if not self.collection:
            return {
                "exists": False,
                "count": 0
            }
        
        count = self.collection.count()
        
        return {
            "exists": True,
            "count": count,
            "name": self.collection_name
        }
