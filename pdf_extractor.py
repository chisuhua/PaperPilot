"""
<<<<<<< HEAD
PDF Extractor Module
使用 pymupdf 提取 PDF 文本和元数据
"""
import os
from typing import Dict, Optional, List
from pathlib import Path
import re
import fitz  # pymupdf
import logging

logger = logging.getLogger(__name__)


class PDFExtractor:
    """PDF 文本提取器，使用 pymupdf 处理 PDF 文件
    
    相比 PyPDF2，pymupdf 更加鲁棒，能够处理：
    - 复杂布局（多栏、表格）
    - 嵌入的公式和图表
    - 损坏或格式不规范的 PDF
    """
    
    def __init__(self, preserve_layout: bool = False):
        """初始化 PDF 提取器
        
        Args:
            preserve_layout: 是否保留原始布局（默认 False）
        """
        self.preserve_layout = preserve_layout
    
    def extract_text(self, pdf_path: str) -> str:
        """从 PDF 文件中提取文本
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            提取的文本内容
            
        Raises:
            FileNotFoundError: PDF 文件不存在
            PDFExtractionError: PDF 提取失败
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num, page in enumerate(doc):
                try:
                    page_text = page.get_text("text")
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num} from {pdf_path}: {e}")
                    continue
            
            doc.close()
            
            if not text.strip():
                logger.warning(f"No text extracted from {pdf_path}")
            
            return text
            
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {e}")
            raise PDFExtractionError(f"Extraction failed: {e}")
    
    def extract_metadata(self, pdf_path: str) -> Dict[str, Optional[str]]:
        """提取 PDF 元数据（标题、作者、年份等）
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            元数据字典，包含 title, authors, year 等字段
        """
        metadata = {
            'title': None,
            'authors': [],
            'year': None,
            'filename': os.path.basename(pdf_path),
            'pages': 0
        }
        
        try:
            doc = fitz.open(pdf_path)
            metadata['pages'] = len(doc)
            
            # 尝试从 PDF 元数据获取
            pdf_meta = doc.metadata
            if pdf_meta:
                metadata['title'] = pdf_meta.get('title') or None
                author_str = pdf_meta.get('author', '')
                if author_str:
                    metadata['authors'] = [a.strip() for a in author_str.split(',')]
            
            # 如果元数据为空，尝试启发式提取
            if not metadata['title']:
                text = self.extract_text(pdf_path)
                metadata['title'] = self._extract_title_heuristic(text)
                metadata['year'] = self._extract_year_heuristic(text)
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Failed to extract metadata from {pdf_path}: {e}")
        
        return metadata
    
    def _extract_title_heuristic(self, text: str) -> Optional[str]:
        """启发式提取标题（从文本前几行）
        
        Args:
            text: PDF 文本内容
            
        Returns:
            提取的标题或 None
        """
        lines = [l.strip() for l in text.split('\n')[:15] if l.strip()]
        
        # 找到第一个足够长的非空行作为标题
        for line in lines:
            # 跳过看起来像页眉/页脚的行
            if len(line) < 10 or len(line) > 200:
                continue
            # 跳过纯数字或日期
            if line.isdigit() or re.match(r'^\d{4}[-/]\d{1,2}', line):
                continue
            # 跳过 URL
            if 'http' in line.lower() or 'www' in line.lower():
                continue
            
            return line
        
        return "Untitled"
    
    def _extract_year_heuristic(self, text: str) -> Optional[int]:
        """启发式提取年份
        
        Args:
            text: PDF 文本内容
            
        Returns:
            提取的年份或 None
        """
        # 在前 1000 字符中查找 2000-2030 之间的年份
        text_sample = text[:1000]
        year_pattern = r'\b(20[0-3][0-9])\b'
        matches = re.findall(year_pattern, text_sample)
        
        if matches:
            # 返回最常见的年份
            from collections import Counter
            year_counts = Counter(matches)
            most_common_year = year_counts.most_common(1)[0][0]
            return int(most_common_year)
        
        return None
    
    def extract_with_metadata(self, pdf_path: str) -> Dict:
        """同时提取文本和元数据
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            包含 text 和 metadata 的字典
        """
        text = self.extract_text(pdf_path)
        metadata = self.extract_metadata(pdf_path)
        
        return {
            'text': text,
            'metadata': metadata,
            'path': pdf_path
        }


class PDFExtractionError(Exception):
    """PDF 提取错误"""
    pass
=======
PDF text extraction module using PyMuPDF (fitz).
Extracts text and metadata from PDF files.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Dict, List, Optional


class PDFExtractor:
    """Extract text and metadata from PDF files."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF extractor.
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
    
    def extract_text(self) -> str:
        """
        Extract all text from the PDF.
        
        Returns:
            Complete text content from all pages
        """
        text_parts = []
        for page in self.doc:
            text_parts.append(page.get_text())
        return "\n".join(text_parts)
    
    def extract_metadata(self) -> Dict[str, Optional[str]]:
        """
        Extract metadata from the PDF.
        
        Returns:
            Dictionary containing title, author, subject, keywords, etc.
        """
        metadata = self.doc.metadata
        
        # Try to extract year from creation date or modification date
        year = None
        if metadata.get('creationDate'):
            try:
                # Date format: D:YYYYMMDDHHmmSS
                date_str = metadata['creationDate']
                if date_str.startswith('D:') and len(date_str) >= 6:
                    year = date_str[2:6]
            except (ValueError, IndexError, TypeError):
                pass
        
        return {
            'title': metadata.get('title', self.pdf_path.stem),
            'author': metadata.get('author', 'Unknown'),
            'subject': metadata.get('subject', ''),
            'keywords': metadata.get('keywords', ''),
            'year': year,
            'pages': self.doc.page_count,
            'filename': self.pdf_path.name
        }
    
    def close(self):
        """Close the PDF document."""
        self.doc.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
>>>>>>> c82a479
