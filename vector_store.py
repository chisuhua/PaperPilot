"""
Vector storage and semantic search using ChromaDB and sentence-transformers.
Handles document embedding and similarity search.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import uuid


class VectorStore:
    """Manage vector embeddings and semantic search."""
    
    def __init__(self, model_name: str = "BAAI/bge-m3", collection_name: str = "papers"):
        """
        Initialize vector store.
        
        Args:
            model_name: Name of the sentence-transformers model
            collection_name: Name of the ChromaDB collection
        """
        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Initialize ChromaDB in-memory
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[Dict]] = None,
                     ids: Optional[List[str]] = None):
        """
        Add documents to the vector store.
        
        Args:
            texts: List of text chunks to embed and store
            metadatas: Optional list of metadata dictionaries for each text
            ids: Optional list of unique IDs for each document
        """
        if not texts:
            return
        
        # Generate IDs if not provided
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas if metadatas else [{}] * len(texts),
            ids=ids
        )
        print(f"Added {len(texts)} documents to vector store")
    
    def search(self, query: str, n_results: int = 5) -> Dict:
        """
        Perform semantic search.
        
        Args:
            query: Natural language query
            n_results: Number of results to return
            
        Returns:
            Dictionary containing documents, distances, and metadata
        """
        # Generate query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        return results
    
    def get_collection_info(self) -> Dict:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            "name": self.collection.name,
            "count": count,
            "metadata": self.collection.metadata
        }
    
    def reset(self):
        """Clear all documents from the collection."""
        self.client.reset()
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"}
        )
