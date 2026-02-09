# PaperPilot Usage Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (first run only, to download embedding model)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- `pymupdf` - PDF text extraction
- `sentence-transformers` - Text embeddings
- `chromadb` - Vector database
- `streamlit` - Web interface
- `numpy` - Numerical operations

**Note**: On first run, the BAAI/bge-m3 model (~2.2GB) will be automatically downloaded.

### Step 2: Verify Installation
```bash
python test_components.py
```

Expected output:
```
PaperPilot Component Tests
======================================================================
Testing imports...
  ✓ PyMuPDF 1.26.7
  ✓ ChromaDB
  ✓ Streamlit
  ✓ Sentence-transformers
...
✓ All tests passed!
```

## Usage

### Option 1: Web Interface (Recommended)

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Open browser** at http://localhost:8501

3. **Initialize system**:
   - Click "🚀 初始化系统" in the sidebar
   - Wait for the embedding model to load (first run only)

4. **Load papers**:
   - Upload PDF files using the file uploader, OR
   - Specify a directory path containing PDFs

5. **Search**:
   - Enter a natural language query
   - View results with relevance scores
   - Explore matched text segments

### Option 2: Python API

```python
from paper_manager import PaperManager

# Initialize the system
manager = PaperManager(
    chunk_size=512,     # Characters per chunk
    overlap=50,         # Overlap between chunks
    model_name="BAAI/bge-m3"
)

# Add a single paper
paper_id = manager.add_paper("path/to/paper.pdf")

# Or add multiple papers from a directory
paper_ids = manager.add_papers_from_directory("path/to/papers/")

# Search with natural language
results = manager.search(
    query="deep learning for image recognition",
    n_results=5
)

# Process results
for result in results:
    print(f"Title: {result['title']}")
    print(f"Author: {result['author']}")
    print(f"Year: {result['year']}")
    print(f"Relevance: {result['relevance_score']:.2%}")
    print(f"Text: {result['text'][:200]}...")
    print("-" * 80)

# Get collection statistics
stats = manager.get_stats()
print(f"Total papers: {stats['total_papers']}")
print(f"Total chunks: {stats['total_chunks']}")
```

### Option 3: Interactive CLI

```bash
python example.py
```

Follow the prompts to:
1. Add papers from the `papers/` directory
2. Enter search queries
3. View results interactively

## Examples

### Example 1: Literature Review

```python
from paper_manager import PaperManager

manager = PaperManager()
manager.add_papers_from_directory("~/Documents/research_papers/")

# Find papers about specific topics
queries = [
    "transformer architecture attention mechanism",
    "convolutional neural networks for object detection",
    "transfer learning in NLP",
]

for query in queries:
    print(f"\nQuery: {query}")
    results = manager.search(query, n_results=3)
    for r in results:
        print(f"  - {r['title']} ({r['relevance_score']:.2%})")
```

### Example 2: Extract Methodology

```python
manager = PaperManager()
manager.add_paper("paper.pdf")

# Find methodology sections
results = manager.search(
    "experimental setup methodology dataset evaluation metrics",
    n_results=5
)

for result in results:
    if result['relevance_score'] > 0.7:
        print(f"From {result['title']}:")
        print(result['text'])
```

### Example 3: Compare Papers

```python
manager = PaperManager()
manager.add_papers_from_directory("comparison_papers/")

# Find similar content across papers
query = "what are the main challenges in reinforcement learning"
results = manager.search(query, n_results=10)

# Group by paper
papers = {}
for r in results:
    title = r['title']
    if title not in papers:
        papers[title] = []
    papers[title].append(r)

for title, chunks in papers.items():
    print(f"\n{title}:")
    print(f"  Found {len(chunks)} relevant segments")
```

## Configuration

### Chunking Parameters

Adjust in `PaperManager` initialization:

```python
manager = PaperManager(
    chunk_size=512,    # Larger = more context, fewer chunks
    overlap=50,        # More overlap = better continuity
)
```

**Recommendations**:
- Short papers (< 10 pages): `chunk_size=256, overlap=30`
- Normal papers (10-30 pages): `chunk_size=512, overlap=50` (default)
- Long papers (> 30 pages): `chunk_size=1024, overlap=100`

### Embedding Model

Choose different models for specific needs:

```python
# Default: Best multilingual performance
manager = PaperManager(model_name="BAAI/bge-m3")

# English-only, faster
manager = PaperManager(model_name="all-MiniLM-L6-v2")

# High quality, slower
manager = PaperManager(model_name="BAAI/bge-large-en-v1.5")
```

## Troubleshooting

### Issue: Model download fails

**Solution**: Check internet connection and try:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3')"
```

### Issue: PDF extraction returns empty text

**Cause**: Scanned PDFs (images) without OCR
**Solution**: Use OCR preprocessing or text-based PDFs

### Issue: Out of memory

**Cause**: Too many papers loaded at once
**Solution**: Process papers in batches or increase system RAM

### Issue: Search results not relevant

**Solution**: Try:
1. More specific queries
2. Adjust chunk_size for better context
3. Use technical terms from the domain

## Best Practices

1. **Organize papers by topic** in different directories
2. **Use descriptive queries** with domain-specific terminology
3. **Iterate on queries** based on initial results
4. **Check relevance scores** - ignore results below 0.5
5. **Keep PDFs text-based** for best extraction quality

## Performance

Typical performance on modern hardware:

- **PDF extraction**: ~1-2 seconds per paper
- **Chunking**: < 0.1 seconds
- **Embedding**: ~0.5-1 second per chunk
- **Search**: < 0.1 seconds
- **Model loading**: ~5-10 seconds (first time only)

For 100 papers (~10 pages each):
- Initial processing: ~10-15 minutes
- Subsequent searches: < 1 second

## Support

For issues or questions:
- Check existing GitHub issues
- Open a new issue with detailed description
- Include Python version and error messages
