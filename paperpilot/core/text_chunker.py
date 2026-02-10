"""
Text Chunker Module
将文本分割成固定长度的块，支持重叠
"""
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class TextChunker:
    """文本分块器，使用固定长度和重叠策略
    
    固定长度分块比段落分割更加可控和一致，
    有利于后续的嵌入和检索。
    """
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        """初始化分块器
        
        Args:
            chunk_size: 每个块的字符数（默认 512）
            overlap: 块之间重叠的字符数（默认 50）
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if overlap < 0:
            raise ValueError("overlap cannot be negative")
        if overlap >= chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        
        self.chunk_size = chunk_size
        self.overlap = overlap
        logger.debug(f"TextChunker initialized: chunk_size={chunk_size}, overlap={overlap}")
    
    def chunk(self, text: str) -> List[str]:
        """将文本分割成块
        
        Args:
            text: 输入文本
            
        Returns:
            文本块列表
        """
        if not text or not text.strip():
            logger.warning("Empty text provided to chunker")
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # 只添加非空块
            if chunk.strip():
                chunks.append(chunk)
            
            # 移动到下一个位置（考虑重叠）
            start += self.chunk_size - self.overlap
        
        logger.debug(f"Chunked text into {len(chunks)} chunks")
        return chunks
    
    def chunk_with_metadata(self, text: str, source: str = "") -> List[Tuple[str, dict]]:
        """分块并附加元数据
        
        Args:
            text: 输入文本
            source: 来源标识（如文件名）
            
        Returns:
            (chunk, metadata) 元组列表
        """
        chunks = self.chunk(text)
        
        result = []
        for i, chunk in enumerate(chunks):
            metadata = {
                'source': source,
                'chunk_index': i,
                'chunk_size': len(chunk),
                'total_chunks': len(chunks)
            }
            result.append((chunk, metadata))
        
        return result
    
    def smart_chunk(self, text: str, try_sentence_boundaries: bool = True) -> List[str]:
        """智能分块：尽量在句子边界处分割
        
        Args:
            text: 输入文本
            try_sentence_boundaries: 是否尝试在句子边界分割（默认 True）
            
        Returns:
            文本块列表
        """
        if not try_sentence_boundaries:
            return self.chunk(text)
        
        chunks = []
        start = 0
        text_length = len(text)
        
        # 句子结束标记
        sentence_ends = ['. ', '。', '! ', '！', '? ', '？', '\n\n']
        
        while start < text_length:
            end = start + self.chunk_size
            
            if end >= text_length:
                # 最后一块
                chunk = text[start:]
                if chunk.strip():
                    chunks.append(chunk)
                break
            
            # 在块的后 20% 范围内查找句子边界
            search_start = int(end * 0.8)
            search_end = min(end + 50, text_length)
            search_region = text[search_start:search_end]
            
            # 寻找最近的句子结束标记
            best_position = -1
            for marker in sentence_ends:
                pos = search_region.find(marker)
                if pos != -1:
                    actual_pos = search_start + pos + len(marker)
                    if best_position == -1 or actual_pos < best_position:
                        best_position = actual_pos
            
            if best_position != -1:
                # 在句子边界处分割
                chunk = text[start:best_position]
                start = best_position
            else:
                # 没找到边界，使用固定长度
                chunk = text[start:end]
                start = end - self.overlap
            
            if chunk.strip():
                chunks.append(chunk)
        
        logger.debug(f"Smart chunked text into {len(chunks)} chunks")
        return chunks
