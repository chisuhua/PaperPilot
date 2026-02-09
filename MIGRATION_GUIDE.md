# 架构迁移指南

## 🎯 目标

从当前实现（v1）迁移到 PLAN.md 建议架构（v2），实现更强大、可扩展的论文管理系统。

---

## 📊 关键差异速查表

### 核心变更

| 组件 | v1 (当前) | v2 (PLAN.md) | 迁移难度 |
|------|-----------|--------------|---------|
| PDF 解析 | PyPDF2 | pymupdf | 🟢 简单 |
| 嵌入模型 | MiniLM-L12-v2 | bge-m3 | 🟢 简单 |
| 向量存储 | numpy 数组 | ChromaDB | 🟡 中等 |
| 分块策略 | 段落分割 | 固定长度+重叠 | 🟢 简单 |
| 持久化 | ❌ 无 | ✅ 自动 | 🟢 简单 |

---

## 🔄 逐步迁移方案

### 方案 A：渐进式迁移（推荐）

**适用场景**：生产环境有现有用户

```
Week 1: 新建 v2 分支，实现核心功能
Week 2: 并行运行 v1 和 v2，A/B 测试
Week 3: 数据迁移，全面切换到 v2
```

**优点**：
- ✅ 风险可控
- ✅ 用户无感知
- ✅ 可随时回滚

**缺点**：
- ⚠️ 需要维护两套代码
- ⚠️ 迁移周期较长

---

### 方案 B：直接重写（快速）

**适用场景**：无生产数据，或用户可容忍停机

```
Day 1-2: 按 PLAN.md 实现新架构
Day 3: 测试验证
Day 4: 一次性切换
```

**优点**：
- ✅ 快速完成
- ✅ 代码简洁

**缺点**：
- ⚠️ 有停机时间
- ⚠️ 需要数据迁移脚本

---

## 📝 详细迁移步骤

### Step 1: 环境准备

```bash
# 安装新依赖
pip install pymupdf chromadb

# 可选：创建虚拟环境隔离测试
python -m venv venv_v2
source venv_v2/bin/activate
pip install -r requirements_v2.txt
```

### Step 2: 创建新模块结构

```
PaperPilot/
├── v1/                    # 保留当前实现
│   ├── pdf_processor.py
│   ├── search_engine.py
│   └── app.py
├── v2/                    # 新架构
│   ├── pdf_extractor.py   # 使用 pymupdf
│   ├── text_chunker.py    # 固定长度分块
│   ├── vector_store.py    # ChromaDB 封装
│   └── app.py             # 更新的 UI
└── migration/             # 迁移工具
    └── import_from_v1.py
```

### Step 3: 实现核心模块

#### 3.1 PDF 提取器（v2/pdf_extractor.py）

```python
import fitz  # pymupdf

class PDFExtractor:
    def extract_text(self, pdf_path: str) -> str:
        """使用 pymupdf 提取文本，比 PyPDF2 更鲁棒"""
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_with_metadata(self, pdf_path: str) -> dict:
        """同时提取文本和元数据"""
        doc = fitz.open(pdf_path)
        return {
            'text': ''.join(page.get_text() for page in doc),
            'pages': len(doc),
            'metadata': doc.metadata
        }
```

#### 3.2 文本分块器（v2/text_chunker.py）

```python
class TextChunker:
    def __init__(self, chunk_size=512, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str) -> list[str]:
        """固定长度分块，带重叠"""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks
```

#### 3.3 向量存储（v2/vector_store.py）

```python
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, collection_name="papers"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.model = SentenceTransformer('BAAI/bge-m3')
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, texts: list[str], metadatas: list[dict]):
        """批量添加文档"""
        embeddings = self.model.encode(texts).tolist()
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, top_k=5):
        """语义搜索"""
        query_embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
```

### Step 4: 数据迁移脚本

```python
# migration/import_from_v1.py
from v1.pdf_processor import PDFProcessor as ProcessorV1
from v2.pdf_extractor import PDFExtractor
from v2.text_chunker import TextChunker
from v2.vector_store import VectorStore

def migrate_documents():
    """从 v1 数据导入到 v2"""
    # 1. 读取 v1 已处理的文档
    processor_v1 = ProcessorV1()
    # （假设有保存的文件列表）
    
    # 2. 使用 v2 组件重新处理
    extractor = PDFExtractor()
    chunker = TextChunker()
    store = VectorStore()
    
    for pdf_path in get_v1_documents():
        text = extractor.extract_text(pdf_path)
        chunks = chunker.chunk(text)
        metadatas = [{"source": pdf_path}] * len(chunks)
        store.add_documents(chunks, metadatas)
    
    print("迁移完成！")
```

### Step 5: 更新 Streamlit UI

主要变更：
1. 使用 `VectorStore` 替代 `SemanticSearchEngine`
2. 数据自动持久化（无需重新索引）
3. 支持增量添加文档

```python
# v2/app.py 关键差异
if st.button("处理 PDF"):
    # v1 方式：全部重新处理
    # processor.process_multiple_pdfs(files)
    
    # v2 方式：增量添加
    for file in new_files:
        text = extractor.extract_text(file)
        chunks = chunker.chunk(text)
        store.add_documents(chunks, [{"source": file.name}])
    st.success("已添加到索引！")  # 自动持久化
```

---

## 🧪 测试验证

### 功能对比测试

```python
# tests/compare_v1_v2.py
def test_search_quality():
    """对比 v1 和 v2 的搜索结果"""
    queries = [
        "深度学习的应用",
        "transformer 架构",
        "attention mechanism"
    ]
    
    for query in queries:
        results_v1 = search_v1(query)
        results_v2 = search_v2(query)
        
        # 对比相似度分数
        # 对比返回文档的相关性
```

### 性能基准测试

```python
import time

def benchmark():
    docs = load_test_documents(count=1000)
    
    # 测试索引速度
    start = time.time()
    index_v1(docs)
    t1 = time.time() - start
    
    start = time.time()
    index_v2(docs)
    t2 = time.time() - start
    
    print(f"v1 索引时间: {t1:.2f}s")
    print(f"v2 索引时间: {t2:.2f}s")
```

---

## 🎓 最佳实践

### 1. 配置管理

创建 `config.yaml` 统一管理参数：

```yaml
model:
  name: "BAAI/bge-m3"
  cache_dir: "./models"

chunking:
  chunk_size: 512
  overlap: 50

chromadb:
  persist_directory: "./chroma_db"
  collection_name: "papers"
```

### 2. 日志系统

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('paperpilot.log'),
        logging.StreamHandler()
    ]
)
```

### 3. 错误处理

```python
class PDFProcessingError(Exception):
    pass

def safe_extract(pdf_path):
    try:
        return extractor.extract_text(pdf_path)
    except Exception as e:
        logger.error(f"Failed to process {pdf_path}: {e}")
        raise PDFProcessingError(f"Cannot process {pdf_path}")
```

---

## ⚠️ 常见问题

### Q1: 模型太大，下载失败怎么办？

**A**: 使用国内镜像或手动下载

```python
# 使用 HF_ENDPOINT 环境变量
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

model = SentenceTransformer('BAAI/bge-m3')
```

### Q2: ChromaDB 数据损坏如何恢复？

**A**: 定期备份 + 导出机制

```python
# 导出为 JSON
collection.get()  # 获取所有数据
# 定期备份 ./chroma_db 目录
```

### Q3: v1 和 v2 能否共存？

**A**: 可以，使用不同端口运行

```bash
# v1 运行在 8501
streamlit run v1/app.py --server.port 8501

# v2 运行在 8502
streamlit run v2/app.py --server.port 8502
```

---

## 📞 支持资源

- 技术讨论：[GitHub Issues](https://github.com/chisuhua/PaperPilot/issues)
- 架构对比文档：`ARCHITECTURE_COMPARISON.md`
- PLAN.md：完整开发计划

---

*最后更新*：2026-02-09
