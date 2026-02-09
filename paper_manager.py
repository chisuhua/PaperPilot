"""
Main paper management system that integrates all components.
"""

from pathlib import Path
from typing import List, Dict, Optional
from pdf_extractor import PDFExtractor
from text_chunker import TextChunker
from vector_store import VectorStore


class PaperManager:
    """Intelligent paper management system."""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50,
                 model_name: str = "BAAI/bge-m3"):
        """
        Initialize paper manager.
        
        Args:
            chunk_size: Size of text chunks in characters
            overlap: Overlap between chunks in characters
            model_name: Embedding model name
        """
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
        self.vector_store = VectorStore(model_name=model_name)
        self.papers = {}  # Store paper metadata by ID
    
    def add_paper(self, pdf_path: str) -> str:
        """
        Add a paper to the system.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Paper ID
        """
        print(f"\nProcessing: {pdf_path}")
        
        # Extract text and metadata
        with PDFExtractor(pdf_path) as extractor:
            text = extractor.extract_text()
            metadata = extractor.extract_metadata()
        
        print(f"Extracted {len(text)} characters from {metadata['pages']} pages")
        
        # Chunk the text
        chunks = self.chunker.chunk_text(text)
        print(f"Split into {len(chunks)} chunks")
        
        # Generate paper ID
        paper_id = metadata['filename']
        
        # Prepare metadata for each chunk
        chunk_metadatas = []
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            chunk_metadata = {
                'paper_id': paper_id,
                'title': metadata['title'],
                'author': metadata['author'],
                'year': metadata['year'] or '',
                'chunk_index': i,
                'filename': metadata['filename']
            }
            chunk_metadatas.append(chunk_metadata)
            chunk_ids.append(f"{paper_id}_chunk_{i}")
        
        # Add to vector store
        self.vector_store.add_documents(chunks, metadatas=chunk_metadatas, ids=chunk_ids)
        
        # Store paper metadata
        self.papers[paper_id] = metadata
        
        print(f"Successfully added paper: {metadata['title']}")
        return paper_id
    
    def add_papers_from_directory(self, directory: str) -> List[str]:
        """
        Add all PDF papers from a directory.
        
        Args:
            directory: Path to directory containing PDFs
            
        Returns:
            List of paper IDs
        """
        dir_path = Path(directory)
        pdf_files = list(dir_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {directory}")
            return []
        
        print(f"Found {len(pdf_files)} PDF files")
        
        paper_ids = []
        for pdf_file in pdf_files:
            try:
                paper_id = self.add_paper(str(pdf_file))
                paper_ids.append(paper_id)
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {e}")
        
        return paper_ids
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search papers using natural language query.
        
        Args:
            query: Natural language search query
            n_results: Number of results to return
            
        Returns:
            List of search results with text, metadata, and relevance scores
        """
        # Perform vector search
        results = self.vector_store.search(query, n_results=n_results)
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents']) > 0:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0]
            distances = results['distances'][0]
            
            for doc, meta, dist in zip(documents, metadatas, distances):
                result = {
                    'text': doc,
                    'title': meta.get('title', 'Unknown'),
                    'author': meta.get('author', 'Unknown'),
                    'year': meta.get('year', ''),
                    'filename': meta.get('filename', ''),
                    'chunk_index': meta.get('chunk_index', 0),
                    'relevance_score': 1 - dist  # Convert distance to similarity score
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the paper collection.
        
        Returns:
            Dictionary with statistics
        """
        collection_info = self.vector_store.get_collection_info()
        return {
            'total_papers': len(self.papers),
            'total_chunks': collection_info['count'],
            'papers': list(self.papers.values())
        }
