"""
Search Engine Module
使用语义搜索技术实现自然语言搜索功能
"""
from typing import List, Dict, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticSearchEngine:
    """语义搜索引擎，支持自然语言查询"""
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化搜索引擎
        
        Args:
            model_name: 使用的句子嵌入模型名称
                       默认使用支持中英文的多语言模型
        """
        print(f"Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.paragraphs = []
        self.embeddings = None
        print("Model loaded successfully!")
    
    def index_paragraphs(self, paragraphs: List[Tuple[str, str, int]]):
        """
        为段落建立索引
        
        Args:
            paragraphs: (文件名, 段落内容, 段落索引) 的列表
        """
        self.paragraphs = paragraphs
        
        if not paragraphs:
            self.embeddings = None
            return
        
        # 提取段落文本
        paragraph_texts = [para[1] for para in paragraphs]
        
        print(f"Indexing {len(paragraph_texts)} paragraphs...")
        # 生成嵌入向量
        self.embeddings = self.model.encode(paragraph_texts, show_progress_bar=True)
        print("Indexing completed!")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, any]]:
        """
        执行语义搜索
        
        Args:
            query: 搜索查询（自然语言）
            top_k: 返回的结果数量
            
        Returns:
            搜索结果列表，每个结果包含文件名、段落内容、相似度分数等
        """
        if not self.paragraphs or self.embeddings is None:
            return []
        
        # 为查询生成嵌入向量
        query_embedding = self.model.encode([query])
        
        # 计算余弦相似度
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # 获取 top-k 结果
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            filename, paragraph, para_idx = self.paragraphs[idx]
            similarity = float(similarities[idx])
            
            results.append({
                'filename': filename,
                'paragraph': paragraph,
                'paragraph_index': para_idx,
                'similarity_score': similarity
            })
        
        return results
    
    def search_with_threshold(self, query: str, threshold: float = 0.3, 
                             max_results: int = 10) -> List[Dict[str, any]]:
        """
        执行语义搜索，只返回相似度高于阈值的结果
        
        Args:
            query: 搜索查询
            threshold: 相似度阈值
            max_results: 最大结果数量
            
        Returns:
            搜索结果列表
        """
        all_results = self.search(query, top_k=max_results)
        
        # 过滤低于阈值的结果
        filtered_results = [
            result for result in all_results 
            if result['similarity_score'] >= threshold
        ]
        
        return filtered_results
