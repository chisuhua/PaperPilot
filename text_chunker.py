"""
Text chunking module with overlap strategy.
Splits text into fixed-length chunks with configurable overlap.
"""

from typing import List


class TextChunker:
    """Split text into overlapping chunks."""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Size of each chunk in characters
            overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        if overlap >= chunk_size:
            raise ValueError("Overlap must be smaller than chunk size")
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk)
            
            # Move start position forward by (chunk_size - overlap)
            start += self.chunk_size - self.overlap
            
            # Break if we've processed all text
            if end >= text_length:
                break
        
        return chunks
