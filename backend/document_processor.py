"""
Document processing utilities for extracting text from various file formats.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any
import PyPDF2


class DocumentProcessor:
    """Process and extract text from various document formats"""
    
    @staticmethod
    def process_file(file_path: str) -> Dict[str, Any]:
        """
        Process a file and extract its content.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary with 'content', 'metadata', and 'source' keys
        """
        file_extension = Path(file_path).suffix.lower()
        file_name = Path(file_path).name
        
        try:
            if file_extension in ['.txt', '.md']:
                content = DocumentProcessor._process_text_file(file_path)
            elif file_extension == '.json':
                content = DocumentProcessor._process_json_file(file_path)
            elif file_extension == '.pdf':
                content = DocumentProcessor._process_pdf_file(file_path)
            elif file_extension in ['.html', '.htm']:
                content = DocumentProcessor._process_html_file(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            return {
                "content": content,
                "metadata": {
                    "source": file_name,
                    "file_type": file_extension,
                    "file_path": file_path
                },
                "source": file_name
            }
        except Exception as e:
            raise Exception(f"Error processing file {file_name}: {str(e)}")
    
    @staticmethod
    def _process_text_file(file_path: str) -> str:
        """Process plain text or markdown files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def _process_json_file(file_path: str) -> str:
        """Process JSON files and convert to readable text"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON to formatted string
        return json.dumps(data, indent=2)
    
    @staticmethod
    def _process_pdf_file(file_path: str) -> str:
        """Process PDF files and extract text"""
        text_content = []
        
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(f"--- Page {page_num + 1} ---\n{text}")
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        
        return "\n\n".join(text_content)
    
    @staticmethod
    def _process_html_file(file_path: str) -> str:
        """Process HTML files"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Split text into chunks with overlap.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for paragraph break
                last_para = text[start:end].rfind('\n\n')
                if last_para > chunk_size * 0.5:  # At least 50% through
                    end = start + last_para + 2
                else:
                    # Look for sentence break
                    last_period = max(
                        text[start:end].rfind('. '),
                        text[start:end].rfind('.\n'),
                        text[start:end].rfind('!\n'),
                        text[start:end].rfind('?\n')
                    )
                    if last_period > chunk_size * 0.5:
                        end = start + last_period + 2
            
            chunks.append(text[start:end].strip())
            
            # Move start position with overlap
            start = end - chunk_overlap if end < len(text) else end
        
        return chunks
    
    @staticmethod
    def extract_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from a file"""
        file_stats = os.stat(file_path)
        
        return {
            "filename": Path(file_path).name,
            "extension": Path(file_path).suffix,
            "size_bytes": file_stats.st_size,
            "created_time": file_stats.st_ctime,
            "modified_time": file_stats.st_mtime
        }
