非常好！下面是一个**可执行、可验收、分阶段演进**的开发计划，专为「个人/小团队论文自动整理 + 分类 + 语义搜索」系统设计。整个计划从 **MVP（最小可行产品）** 开始，逐步扩展至功能完整的 V1.5 系统。

---

## 🎯 总体目标
构建一个本地运行的智能论文管理系统，支持：
- 自动摄入 PDF 论文
- 提取元数据（标题、年份等）
- 向量化存储
- 语义搜索（自然语言）
- 自动聚类分类
- Web 界面交互

> 技术栈原则：**全开源 + 本地优先 + 低依赖**

---

# ✅ 阶段一：MVP（最小可行产品）—— 第1天完成

### 📌 目标
用自然语言搜索本地单篇或多篇 PDF 论文的内容，返回相关段落。

---

### 🔧 架构实现（量化）
| 模块 | 技术选型 | 说明 |
|------|--------|------|
| 文本提取 | `pymupdf` (fitz) | 比 PyPDF2 更鲁棒，支持表格/公式保留 |
| 嵌入模型 | `BAAI/bge-m3` via `sentence-transformers` | 开源 SOTA 多语言嵌入模型 |
| 向量库 | `ChromaDB` (in-memory) | 轻量，无需部署，Python 原生支持 |
| 前端 | `Streamlit` | 快速构建 UI，10 行代码出搜索框 |
| 分块策略 | 固定长度（512 字符，重叠 50） | 简单有效 |

---

### 💻 代码功能实现（核心逻辑）

```python
# ingest.py
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=512, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks

# search.py
client = chromadb.Client()
model = SentenceTransformer('BAAI/bge-m3')

collection = client.create_collection(
    name="papers",
    embedding_function=lambda texts: model.encode(texts).tolist()
)

# 假设 papers/ 下有多个 PDF
for pdf in Path("papers").glob("*.pdf"):
    text = extract_text(pdf)
    chunks = chunk_text(text)
    collection.add(
        documents=chunks,
        metadatas=[{"source": str(pdf)}] * len(chunks),
        ids=[f"{pdf.stem}_{i}" for i in range(len(chunks))]
    )

# query
results = collection.query(query_texts=["How does diffusion model work?"], n_results=3)
```

Streamlit 界面（`app.py`）：
```python
import streamlit as st
query = st.text_input("Search your papers...")
if query:
    results = collection.query(query_texts=[query], n_results=3)
    for doc in results['documents'][0]:
        st.write(doc[:300] + "...")
```

---

### ✅ 验收标准（必须全部通过）
| 编号 | 验收项 | 预期结果 |
|------|--------|--------|
| MVP-1 | 能成功读取 1 篇 PDF（如 arXiv 论文） | 无报错，提取出 >1000 字文本 |
| MVP-2 | 成功将文本分块并存入 ChromaDB | `collection.count()` 返回正确块数 |
| MVP-3 | 输入自然语言查询（如 “What is transformer?”） | 返回 3 个相关段落，内容与问题语义匹配 |
| MVP-4 | Streamlit 界面可本地运行 | `streamlit run app.py` 打开浏览器可搜索 |

> ⏱️ 预计耗时：2–4 小时（含环境安装）

---

# 🚀 阶段二：V0.5 —— 支持批量导入 + 元数据提取（第2天）

### 📌 目标
自动处理整个文件夹的 PDF，提取标题、年份，并在搜索结果中显示。

---

### 🔧 架构变更
| 模块 | 升级点 |
|------|-------|
| 元数据提取 | 新增：用正则 + 启发式规则提取标题/年份（暂不用 GROBID） |
| 存储结构 | ChromaDB 的 `metadatas` 增加 `title`, `year` 字段 |
| 文件监控 | 支持一次性导入 `papers/` 目录下所有 PDF |

---

### 💻 新增代码功能
```python
def extract_title_and_year(text):
    # 简单启发式：前 200 字找年份（2010–2026）
    import re
    year_match = re.search(r'\b(20[1-2][0-9])\b', text[:500])
    year = year_match.group(1) if year_match else "Unknown"
    
    # 标题：假设第一行非空且较长
    lines = [l.strip() for l in text.split('\n')[:10] if l.strip()]
    title = lines[0] if lines and len(lines[0]) > 10 else "Untitled"
    return title, year
```

更新 `collection.add()` 的 `metadatas`：
```python
metadatas=[{"source": str(pdf), "title": title, "year": year}] * len(chunks)
```

Streamlit 显示：
```python
for i, doc in enumerate(results['documents'][0]):
    meta = results['metadatas'][0][i]
    st.markdown(f"**{meta['title']}** ({meta['year']})")
    st.write(doc[:300] + "...")
```

---

### ✅ 验收标准
| 编号 | 验收项 |
|------|--------|
| V0.5-1 | 导入 5 篇不同年份 PDF，系统自动提取标题和年份 |
| V0.5-2 | 搜索结果中显示论文标题和年份 |
| V0.5-3 | 支持重复运行（避免重复插入）→ 加简单去重（按文件名） |

> ⏱️ 耗时：1 天

---

# 🧠 阶段三：V1.0 —— 自动分类 + 摘要生成（第3–5天）

### 📌 目标
- 对论文自动聚类（如“大模型”、“CV”、“生物”）
- 用户可按类别筛选
- 每篇论文生成一句话摘要

---

### 🔧 架构升级
| 模块 | 技术方案 |
|------|--------|
| 聚类 | `HDBSCAN` on paper-level embeddings（用摘要或前 1024 字） |
| 类别命名 | 调用本地 LLM（Ollama + Qwen2）生成簇标签 |
| 摘要生成 | 对每篇论文调用 `qwen:1.8b` 生成摘要 |
| 存储 | ChromaDB 新增 `category`, `summary` 字段 |

---

### 💻 关键实现
1. **Paper-level embedding**：
   ```python
   paper_emb = model.encode(paper_abstract_or_intro)
   ```
2. **聚类 & 标签生成**：
   ```python
   import hdbscan
   clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
   labels = clusterer.fit_predict(all_paper_embs)
   
   # 对每个簇，取 top3 论文标题，让 LLM 命名
   prompt = f"这些论文的主题是什么？\n{titles}\n回答一个2-4字的中文类别名："
   category = ollama.generate(model='qwen:1.8b', prompt=prompt)['response']
   ```
3. 更新元数据，前端增加分类筛选下拉框。

---

### ✅ 验收标准
| 编号 | 验收项 |
|------|--------|
| V1.0-1 | 10+ 篇跨领域论文被分为 ≥2 个合理簇（人工判断） |
| V1.0-2 | 每个簇有可读中文标签（如“语言模型”、“图像分割”） |
| V1.0-3 | 每篇论文在 UI 中显示自动生成的摘要（≤2 句） |
| V1.0-4 | 可按类别筛选搜索结果 |

> ⏱️ 耗时：2–3 天（需安装 Ollama + Qwen）

---

# 🌐 阶段四：V1.5 —— 产品化增强（第6–10天）

### 📌 目标
提升用户体验与自动化程度

---

### 🔧 功能清单
| 功能 | 实现方式 | 验收标准 |
|------|--------|--------|
| PDF 预览 | 前端嵌入 `pdf.js` 或使用 `streamlit-pdf-viewer` | 点击结果可查看原 PDF 对应页 |
| 自动去重 | 基于标题 + 年份哈希 | 重复 PDF 不重复入库 |
| 定时同步 arXiv | 用 `arxiv` Python 包 + cron | 每天自动下载关键词新论文 |
| 响应式 UI | 改用 Gradio 或 FastAPI+React | 手机可访问，加载 <2s |
| 持久化存储 | ChromaDB 持久化到磁盘 | 重启后数据不丢失 |

---

### ✅ 最终验收（V1.5）
| 编号 | 验收项 |
|------|--------|
| V1.5-1 | 系统可 7×24 运行，支持 100+ 篇论文管理 |
| V1.5-2 | 用户可通过 Web 界面完成：上传、搜索、分类浏览、PDF 查看 |
| V1.5-3 | 所有组件本地运行，无需互联网（除初始模型下载） |
| V1.5-4 | 代码模块化，新增功能只需修改单一文件 |

---

## 📦 附：环境依赖清单（MVP 起步）

```bash
pip install pymupdf sentence-transformers chromadb streamlit
# 后续加：
pip install hdbscan ollama arxiv streamlit-pdf-viewer
```

> 模型首次运行会自动下载 BGE-M3（~2.2GB），建议提前准备。

---

## ✅ 总结：为什么这个计划可行？

- **每天都有可见产出** → 保持动力
- **每步可独立验证** → 避免“大爆炸式失败”
- **技术栈聚焦** → 不分散精力
- **完全可控** → 未来可迁移到 Docker / 云服务器

---

如果你同意，我可以：
1. **现在就提供 MVP 的完整可运行代码包（含 `app.py`, `ingest.py`）**
2. 或生成一个 GitHub 仓库模板结构

请告诉我你的选择！
