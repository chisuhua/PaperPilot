# PaperPilot GitHub Copilot Instructions

You are GitHub Copilot, an AI coding assistant for the PaperPilot project - a semantic PDF search system for academic papers.

## Project Overview

PaperPilot is a local-first, intelligent paper management system that enables:
- Natural language search across PDF documents (Chinese & English)
- Semantic embedding-based retrieval
- Metadata extraction (titles, years, authors)
- Automatic classification and clustering
- Document summarization

## Architecture (PLAN.md Based)

### Core Technology Stack

1. **PDF Processing**: `pymupdf` (fitz)
   - More robust than PyPDF2
   - Preserves tables, formulas, and complex layouts
   - Better error handling for malformed PDFs

2. **Embedding Model**: `BAAI/bge-m3` via sentence-transformers
   - SOTA multilingual model (MTEB Top 3)
   - ~85% retrieval accuracy vs 75% for alternatives
   - 2.2GB model size, requires download on first run

3. **Vector Database**: `ChromaDB`
   - Persistent storage (data survives restarts)
   - Supports incremental indexing
   - Built-in ANN (Approximate Nearest Neighbor) search
   - Metadata filtering capabilities

4. **Text Chunking**: Fixed-length with overlap
   - Default: 512 characters per chunk
   - 50 character overlap between chunks
   - Configurable via parameters

5. **Frontend**: Streamlit
   - Rapid UI development
   - Interactive widgets for search and filtering

### Module Structure

```
PaperPilot/
├── pdf_extractor.py      # PDF text extraction using pymupdf
├── text_chunker.py       # Text chunking with overlap
├── vector_store.py       # ChromaDB wrapper
├── paper_manager.py      # High-level API
├── app.py               # Streamlit UI
├── config.yaml          # Configuration management
└── tests/               # Test suite
```

## Coding Guidelines

### 1. Code Style

- **Python Version**: 3.8+
- **Type Hints**: Always use type annotations
- **Docstrings**: Google style docstrings for all public functions
- **Imports**: Group stdlib, third-party, local imports
- **Line Length**: 88 characters (Black formatter)

Example:
```python
from typing import List, Dict, Optional
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer

class PDFExtractor:
    """Extract text from PDF files using pymupdf.
    
    This extractor handles complex PDF layouts including tables,
    formulas, and multi-column text.
    
    Attributes:
        preserve_layout: Whether to preserve original layout
    """
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text content
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            PDFExtractionError: If extraction fails
        """
        pass
```

### 2. Error Handling

Always handle potential errors gracefully:

```python
try:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
except FileNotFoundError:
    logger.error(f"PDF file not found: {pdf_path}")
    raise
except Exception as e:
    logger.error(f"Failed to extract text from {pdf_path}: {e}")
    raise PDFExtractionError(f"Extraction failed: {e}")
```

### 3. Configuration Management

Use `config.yaml` for all configurable parameters:

```yaml
model:
  name: "BAAI/bge-m3"
  cache_dir: "./models"

chunking:
  chunk_size: 512
  overlap: 50

chromadb:
  persist_directory: "./chroma_db"
  collection_name: "papers"
  
logging:
  level: "INFO"
  file: "paperpilot.log"
```

Load config with:
```python
import yaml
with open('config.yaml') as f:
    config = yaml.safe_load(f)
```

### 4. Logging

Use structured logging throughout:

```python
import logging

logger = logging.getLogger(__name__)

# In functions
logger.info(f"Processing PDF: {pdf_path}")
logger.debug(f"Extracted {len(chunks)} chunks")
logger.error(f"Failed to process: {error}")
```

### 5. Testing

Write tests for all core functionality:

```python
def test_pdf_extraction():
    """Test PDF text extraction."""
    extractor = PDFExtractor()
    text = extractor.extract_text("test.pdf")
    assert len(text) > 0
    assert "expected content" in text
```

### 6. Resource Management

Always clean up resources:

```python
# Use context managers
with tempfile.TemporaryDirectory() as temp_dir:
    # Process files
    pass  # Directory automatically cleaned up

# Close documents
doc = fitz.open(pdf_path)
try:
    # Process
    pass
finally:
    doc.close()
```

## Development Workflow

### Phase 1: MVP (Days 1-2)
- Implement basic PDF extraction (pymupdf)
- Set up ChromaDB collection
- Basic semantic search
- Simple Streamlit UI

### Phase 2: V0.5 (Days 3-5)
- Metadata extraction (title, year, authors)
- Batch import from folders
- Duplicate detection
- Enhanced UI with filters

### Phase 3: V1.0 (Days 6-10)
- Automatic clustering (HDBSCAN)
- Document summarization (local LLM)
- Category management
- Export functionality

## Performance Considerations

1. **Batch Processing**: Process multiple PDFs in batches
2. **Lazy Loading**: Load models only when needed
3. **Caching**: Cache embeddings to avoid recomputation
4. **Indexing**: Use ChromaDB's ANN index for fast search

## Security & Privacy

- **Local-First**: All data stored locally, no cloud dependencies
- **No Telemetry**: Disable model telemetry
- **Sanitization**: Sanitize file paths to prevent directory traversal

## Common Patterns

### Adding a New Document

```python
from paper_manager import PaperManager

manager = PaperManager()
manager.add_document(
    pdf_path="paper.pdf",
    metadata={"title": "...", "year": 2024}
)
```

### Searching

```python
results = manager.search(
    query="deep learning applications",
    top_k=5,
    filters={"year": {"$gte": 2020}}
)
```

### Metadata Extraction

```python
from pdf_extractor import PDFExtractor

extractor = PDFExtractor()
metadata = extractor.extract_metadata(pdf_path)
# Returns: {"title": "...", "authors": [...], "year": 2024}
```

## Migration from V1

When migrating from the current implementation:

1. Keep v1 as `legacy/` branch
2. Import existing data using migration script
3. A/B test performance
4. Gradually switch users

## Troubleshooting

### Model Download Issues
```python
# Use HF mirror in China
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
```

### ChromaDB Persistence
```python
# Ensure persist directory exists
import os
os.makedirs("./chroma_db", exist_ok=True)
```

### Memory Issues
```python
# Process in smaller batches
for batch in chunked(pdf_files, batch_size=10):
    process_batch(batch)
```

## References

- **Architecture Analysis**: ARCHITECTURE_COMPARISON.md
- **Migration Guide**: MIGRATION_GUIDE.md
- **Development Plan**: PLAN.md
- **Recommendations**: RECOMMENDATION.md

## Key Metrics

- **Search Accuracy Target**: ≥85%
- **Query Latency Target**: <100ms for 1000 documents
- **Indexing Speed**: >5 PDFs/minute
- **Memory Usage**: <2GB for 1000 documents

---

When generating code, always:
1. Use the PLAN.md architecture (pymupdf + bge-m3 + ChromaDB)
2. Follow the coding guidelines above
3. Add comprehensive error handling
4. Include type hints and docstrings
5. Consider performance and scalability
6. Write tests for new functionality
