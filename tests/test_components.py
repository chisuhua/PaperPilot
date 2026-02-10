"""
Test script for PaperPilot components.
Verifies that all modules are working correctly.
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all required packages can be imported."""
    print("Testing imports...")
    try:
        import pymupdf as fitz
        print(f"  ✓ PyMuPDF {fitz.__version__}")
    except ImportError as e:
        print(f"  ✗ PyMuPDF import failed: {e}")
        return False
    
    try:
        import chromadb
        print(f"  ✓ ChromaDB")
    except ImportError as e:
        print(f"  ✗ ChromaDB import failed: {e}")
        return False
    
    try:
        import streamlit
        print(f"  ✓ Streamlit")
    except ImportError as e:
        print(f"  ✗ Streamlit import failed: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print(f"  ✓ Sentence-transformers")
    except ImportError as e:
        print(f"  ✗ Sentence-transformers import failed: {e}")
        return False
    
    return True


def test_modules():
    """Test PaperPilot modules."""
    print("\nTesting PaperPilot modules...")
    
    try:
        from paperpilot.core import PDFExtractor
        print("  ✓ pdf_extractor module")
    except ImportError as e:
        print(f"  ✗ pdf_extractor import failed: {e}")
        return False
    
    try:
        from paperpilot.core import TextChunker
        print("  ✓ text_chunker module")
    except ImportError as e:
        print(f"  ✗ text_chunker import failed: {e}")
        return False
    
    try:
        from paperpilot.core import VectorStore
        print("  ✓ vector_store module")
    except ImportError as e:
        print(f"  ✗ vector_store import failed: {e}")
        return False
    
    try:
        from paperpilot.core import PaperManager
        print("  ✓ paper_manager module")
    except ImportError as e:
        print(f"  ✗ paper_manager import failed: {e}")
        return False
    
    return True


def test_text_chunker():
    """Test text chunking functionality."""
    print("\nTesting text chunking...")
    
    try:
        from paperpilot.core import TextChunker
        
        chunker = TextChunker(chunk_size=100, overlap=20)
        text = "This is a test sentence. " * 20
        chunks = chunker.chunk_text(text)
        
        if len(chunks) > 0:
            print(f"  ✓ Created {len(chunks)} chunks from {len(text)} characters")
            return True
        else:
            print("  ✗ No chunks created")
            return False
    except Exception as e:
        print(f"  ✗ Text chunking failed: {e}")
        return False


def test_pdf_extraction():
    """Test PDF extraction with test file."""
    print("\nTesting PDF extraction...")
    
    # Check if test PDF exists
    test_pdf = Path("papers/test_paper.pdf")
    if not test_pdf.exists():
        print("  ⚠ Test PDF not found (papers/test_paper.pdf)")
        print("    Run create_test_pdf.py first or add your own PDF")
        return True  # Not a failure, just skipped
    
    try:
        from paperpilot.core import PDFExtractor
        
        with PDFExtractor(str(test_pdf)) as extractor:
            text = extractor.extract_text()
            metadata = extractor.extract_metadata()
        
        if text and metadata:
            print(f"  ✓ Extracted {len(text)} characters")
            print(f"    Title: {metadata['title']}")
            print(f"    Pages: {metadata['pages']}")
            return True
        else:
            print("  ✗ Extraction returned empty results")
            return False
    except Exception as e:
        print(f"  ✗ PDF extraction failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("PaperPilot Component Tests")
    print("=" * 70)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("PaperPilot Modules", test_modules),
        ("Text Chunking", test_text_chunker),
        ("PDF Extraction", test_pdf_extraction),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"\n✗ {name} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Tests: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All tests passed!")
        print("\nNext steps:")
        print("  1. Run 'python example.py' to test full system")
        print("  2. Run 'streamlit run app.py' to launch web interface")
        return 0
    else:
        print("✗ Some tests failed")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
