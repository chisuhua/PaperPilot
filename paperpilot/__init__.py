"""
PaperPilot - Intelligent Paper Management System

A local, open-source paper management system with semantic search capabilities.
"""

__version__ = "1.0.0"
__author__ = "PaperPilot Contributors"

from .core import (
    PaperManager,
    PDFExtractor,
    TextChunker,
    VectorStore,
    SearchEngine,
    PDFExtractionError,
)

__all__ = [
    "PaperManager",
    "PDFExtractor",
    "TextChunker",
    "VectorStore",
    "SearchEngine",
    "PDFExtractionError",
]
