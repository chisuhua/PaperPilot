"""
PDF Processor Module
处理 PDF 文件，提取文本内容和段落
"""
import os
from typing import List, Dict, Tuple, Any
import PyPDF2
import re


class PDFProcessor:
    """PDF 处理器，用于提取和处理 PDF 文本内容"""
    
    def __init__(self):
        self.documents = {}
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        从 PDF 文件中提取文本
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            提取的文本内容
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text is None:
                        continue
                    text += page_text + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            print(f"Please verify the PDF is not corrupted, password-protected, or inaccessible.")
            return ""
    
    def split_into_paragraphs(self, text: str, min_length: int = 50) -> List[str]:
        """
        将文本分割成段落
        
        Args:
            text: 输入文本
            min_length: 段落最小长度
            
        Returns:
            段落列表
        """
        # 按双换行符或多个换行符分割
        paragraphs = re.split(r'\n\s*\n', text)
        
        # 清理和过滤段落
        cleaned_paragraphs = []
        for para in paragraphs:
            # 移除多余空白符
            para = ' '.join(para.split())
            # 只保留足够长的段落
            if len(para) >= min_length:
                cleaned_paragraphs.append(para)
        
        return cleaned_paragraphs
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        处理单个 PDF 文件
        
        Args:
            pdf_path: PDF 文件路径
            
        Returns:
            包含文件名、文本和段落的字典
        """
        filename = os.path.basename(pdf_path)
        text = self.extract_text_from_pdf(pdf_path)
        paragraphs = self.split_into_paragraphs(text)
        
        doc_info = {
            'filename': filename,
            'path': pdf_path,
            'text': text,
            'paragraphs': paragraphs
        }
        
        # Use full path as key to avoid collisions
        self.documents[pdf_path] = doc_info
        return doc_info
    
    def process_multiple_pdfs(self, pdf_paths: List[str]) -> List[Dict[str, Any]]:
        """
        处理多个 PDF 文件
        
        Args:
            pdf_paths: PDF 文件路径列表
            
        Returns:
            文档信息列表
        """
        results = []
        for pdf_path in pdf_paths:
            doc_info = self.process_pdf(pdf_path)
            results.append(doc_info)
        return results
    
    def get_all_paragraphs(self) -> List[Tuple[str, str, int]]:
        """
        获取所有文档的所有段落
        
        Returns:
            (文件名, 段落内容, 段落索引) 的列表
        """
        all_paragraphs = []
        for filename, doc_info in self.documents.items():
            for idx, para in enumerate(doc_info['paragraphs']):
                all_paragraphs.append((filename, para, idx))
        return all_paragraphs
