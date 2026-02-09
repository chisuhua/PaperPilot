"""
PDF text extraction module using PyMuPDF (fitz).
Extracts text and metadata from PDF files.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Optional


class PDFExtractor:
    """Extract text and metadata from PDF files."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
    
    def extract_text(self) -> str:
        """
        Extract all text from the PDF.
        
        Returns:
            Complete text content from all pages
        """
        text_parts = []
        for page in self.doc:
            text_parts.append(page.get_text())
        return "\n".join(text_parts)
    
    def extract_metadata(self) -> Dict[str, Optional[str]]:
        """
        Extract metadata from the PDF.
        
        Returns:
            Dictionary containing title, author, subject, keywords, etc.
        """
        metadata = self.doc.metadata
        
        # Try to extract year from creation date or modification date
        year = None
        if metadata.get('creationDate'):
            try:
                # Date format: D:YYYYMMDDHHmmSS
                date_str = metadata['creationDate']
                if date_str.startswith('D:') and len(date_str) >= 6:
                    year = date_str[2:6]
            except (ValueError, IndexError, TypeError):
                pass
        
        return {
            'title': metadata.get('title', self.pdf_path.stem),
            'author': metadata.get('author', 'Unknown'),
            'subject': metadata.get('subject', ''),
            'keywords': metadata.get('keywords', ''),
            'year': year,
            'pages': self.doc.page_count,
            'filename': self.pdf_path.name
        }
    
    def close(self):
        """Close the PDF document."""
        self.doc.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
