"""
Paper Manager Module
高层 API，整合 PDF 提取、分块和向量存储
"""
from typing import List, Dict, Optional, Any
from pathlib import Path
import logging
import uuid

from pdf_extractor import PDFExtractor, PDFExtractionError
from text_chunker import TextChunker
from vector_store import VectorStore

logger = logging.getLogger(__name__)


class PaperManager:
    """论文管理器，提供统一的 API
    
    整合了 PDF 提取、文本分块和向量存储，
    简化了论文添加和搜索的流程。
    """
    
    def __init__(
        self,
        collection_name: str = "papers",
        persist_directory: str = "./chroma_db",
        model_name: str = "BAAI/bge-m3",
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ):
        """初始化论文管理器
        
        Args:
            collection_name: ChromaDB 集合名称
            persist_directory: 数据持久化目录
            model_name: 嵌入模型名称
            chunk_size: 文本块大小
            chunk_overlap: 文本块重叠大小
        """
        logger.info("Initializing PaperManager...")
        
        self.extractor = PDFExtractor()
        self.chunker = TextChunker(chunk_size=chunk_size, overlap=chunk_overlap)
        self.vector_store = VectorStore(
            collection_name=collection_name,
            persist_directory=persist_directory,
            model_name=model_name
        )
        
        logger.info("PaperManager initialized successfully")
    
    def add_paper(
        self,
        pdf_path: str,
        custom_metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """添加单篇论文到系统
        
        Args:
            pdf_path: PDF 文件路径
            custom_metadata: 自定义元数据（可选）
            
        Returns:
            处理结果，包含状态和统计信息
        """
        logger.info(f"Adding paper: {pdf_path}")
        
        try:
            # 提取文本和元数据
            doc_data = self.extractor.extract_with_metadata(pdf_path)
            text = doc_data['text']
            metadata = doc_data['metadata']
            
            # 合并自定义元数据
            if custom_metadata:
                metadata.update(custom_metadata)
            
            # 生成唯一的文档 ID
            doc_id = str(uuid.uuid4())
            metadata['doc_id'] = doc_id
            metadata['source'] = pdf_path
            
            # 分块
            chunks = self.chunker.smart_chunk(text)
            
            if not chunks:
                logger.warning(f"No chunks extracted from {pdf_path}")
                return {
                    'success': False,
                    'error': 'No text extracted',
                    'pdf_path': pdf_path
                }
            
            # 为每个块准备元数据
            chunk_metadatas = []
            chunk_ids = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = i
                chunk_metadata['total_chunks'] = len(chunks)
                chunk_metadatas.append(chunk_metadata)
                chunk_ids.append(f"{doc_id}_chunk_{i}")
            
            # 添加到向量存储
            self.vector_store.add_documents(
                texts=chunks,
                metadatas=chunk_metadatas,
                ids=chunk_ids
            )
            
            logger.info(f"Successfully added {len(chunks)} chunks from {pdf_path}")
            
            return {
                'success': True,
                'pdf_path': pdf_path,
                'doc_id': doc_id,
                'chunks_added': len(chunks),
                'metadata': metadata
            }
            
        except PDFExtractionError as e:
            logger.error(f"Failed to extract PDF {pdf_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'pdf_path': pdf_path
            }
        except Exception as e:
            logger.error(f"Unexpected error processing {pdf_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'pdf_path': pdf_path
            }
    
    def add_papers_batch(
        self,
        pdf_paths: List[str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """批量添加论文
        
        Args:
            pdf_paths: PDF 文件路径列表
            show_progress: 是否显示进度
            
        Returns:
            批量处理结果统计
        """
        logger.info(f"Batch adding {len(pdf_paths)} papers")
        
        results = {
            'total': len(pdf_paths),
            'successful': 0,
            'failed': 0,
            'total_chunks': 0,
            'details': []
        }
        
        for i, pdf_path in enumerate(pdf_paths):
            if show_progress:
                print(f"Processing {i+1}/{len(pdf_paths)}: {Path(pdf_path).name}")
            
            result = self.add_paper(pdf_path)
            results['details'].append(result)
            
            if result['success']:
                results['successful'] += 1
                results['total_chunks'] += result['chunks_added']
            else:
                results['failed'] += 1
        
        logger.info(
            f"Batch processing complete: {results['successful']} successful, "
            f"{results['failed']} failed, {results['total_chunks']} total chunks"
        )
        
        return results
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """搜索论文
        
        Args:
            query: 搜索查询（自然语言）
            top_k: 返回结果数量
            filters: 元数据过滤条件（如 {"year": 2024}）
            
        Returns:
            搜索结果列表
        """
        logger.info(f"Searching for: {query}")
        
        results = self.vector_store.search_with_scores(
            query=query,
            top_k=top_k,
            where=filters
        )
        
        logger.info(f"Found {len(results)} results")
        return results
    
    def delete_paper(self, doc_id: str) -> int:
        """删除论文及其所有块
        
        Args:
            doc_id: 文档 ID
            
        Returns:
            删除的块数量
        """
        logger.info(f"Deleting paper: {doc_id}")
        return self.vector_store.delete_by_metadata({"doc_id": doc_id})
    
    def get_stats(self) -> Dict[str, Any]:
        """获取系统统计信息
        
        Returns:
            统计信息字典
        """
        total_chunks = self.vector_store.count()
        
        return {
            'total_chunks': total_chunks,
            'collection_name': self.vector_store.collection_name,
            'model_name': self.vector_store.model_name,
            'chunk_size': self.chunker.chunk_size,
            'chunk_overlap': self.chunker.overlap
        }
    
    def reset(self) -> None:
        """重置系统（删除所有数据）"""
        logger.warning("Resetting PaperManager - all data will be deleted")
        self.vector_store.reset()
