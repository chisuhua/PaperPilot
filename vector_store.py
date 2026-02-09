"""
Vector Store Module
ChromaDB 向量数据库封装
"""
from typing import List, Dict, Optional, Any
import os
import logging
from pathlib import Path

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(
        f"Required package not installed: {e}. "
        "Please run: pip install chromadb sentence-transformers"
    )

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB 向量存储封装
    
    提供持久化向量存储，支持：
    - 自动持久化（数据不会在重启后丢失）
    - 增量添加文档
    - 高效的 ANN 检索
    - 元数据过滤
    """
    
    def __init__(
        self,
        collection_name: str = "papers",
        persist_directory: str = "./chroma_db",
        model_name: str = "BAAI/bge-m3"
    ):
        """初始化向量存储
        
        Args:
            collection_name: ChromaDB 集合名称
            persist_directory: 数据持久化目录
            model_name: 嵌入模型名称（默认 bge-m3）
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.model_name = model_name
        
        # 确保持久化目录存在
        os.makedirs(persist_directory, exist_ok=True)
        
        logger.info(f"Initializing VectorStore with model: {model_name}")
        
        # 初始化 ChromaDB 客户端（持久化模式）
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,  # 禁用遥测
                allow_reset=True
            )
        )
        
        # 加载嵌入模型
        logger.info(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        logger.info("Model loaded successfully!")
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        """批量添加文档到向量存储
        
        Args:
            texts: 文本列表
            metadatas: 元数据列表（可选）
            ids: 文档 ID 列表（可选，自动生成）
        """
        if not texts:
            logger.warning("No texts provided to add_documents")
            return
        
        # 生成 embeddings
        logger.info(f"Generating embeddings for {len(texts)} documents...")
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        # 生成 IDs（如果未提供）
        if ids is None:
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(texts))]
        
        # 确保元数据列表长度匹配
        if metadatas is None:
            metadatas = [{}] * len(texts)
        
        # 添加到集合
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(texts)} documents to collection")
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            where: 元数据过滤条件（可选）
            
        Returns:
            搜索结果字典，包含 documents, metadatas, distances
        """
        if not query or not query.strip():
            logger.warning("Empty query provided")
            return {
                'documents': [[]],
                'metadatas': [[]],
                'distances': [[]],
                'ids': [[]]
            }
        
        # 生成查询 embedding
        query_embedding = self.model.encode([query])[0].tolist()
        
        # 执行搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where  # 元数据过滤
        )
        
        logger.debug(f"Search returned {len(results['documents'][0])} results")
        return results
    
    def search_with_scores(
        self,
        query: str,
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """搜索并返回格式化的结果列表
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            where: 元数据过滤条件
            
        Returns:
            结果列表，每个结果包含 document, metadata, score
        """
        raw_results = self.search(query, top_k, where)
        
        formatted_results = []
        if raw_results['documents'] and raw_results['documents'][0]:
            for i in range(len(raw_results['documents'][0])):
                result = {
                    'document': raw_results['documents'][0][i],
                    'metadata': raw_results['metadatas'][0][i],
                    'distance': raw_results['distances'][0][i],
                    'id': raw_results['ids'][0][i],
                    # 转换距离为相似度分数 (1 - distance for cosine)
                    'similarity_score': 1.0 - raw_results['distances'][0][i]
                }
                formatted_results.append(result)
        
        return formatted_results
    
    def delete_by_metadata(self, where: Dict) -> int:
        """根据元数据删除文档
        
        Args:
            where: 元数据过滤条件
            
        Returns:
            删除的文档数量
        """
        # 先查询匹配的文档
        results = self.collection.get(where=where)
        ids_to_delete = results['ids']
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)
            logger.info(f"Deleted {len(ids_to_delete)} documents")
        
        return len(ids_to_delete)
    
    def count(self) -> int:
        """返回集合中的文档数量"""
        return self.collection.count()
    
    def reset(self) -> None:
        """重置集合（删除所有数据）"""
        logger.warning(f"Resetting collection: {self.collection_name}")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection reset complete")
