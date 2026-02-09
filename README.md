# PaperPilot

开发一个能自动整理、分类并提供搜索功能的论文智能体（Paper Assistant Agent），可以分为以下几个关键模块来设计和实现。以下是一个系统化的开发指南，适用于科研人员、学生或团队构建自己的本地/云端论文管理系统。

---

## 一、整体架构概览

```text
[论文输入] → [预处理] → [元数据提取] → [向量化 & 分类] → [存储] → [搜索接口]
```

主要模块包括：

1. **文档摄入（Ingestion）**
2. **元数据与内容提取（Metadata & Text Extraction）**
3. **文本嵌入与向量化（Embedding）**
4. **自动分类（Classification / Clustering）**
5. **向量数据库存储（Vector DB）**
6. **语义搜索与问答（Search & RAG）**
7. **用户界面（可选：Web / CLI / 插件）**

---

## 二、详细实现步骤

### 1. 文档摄入（支持 PDF、DOCX 等）
- 使用工具：
  - `PyPDF2` / `pdfplumber` / `pymupdf`（推荐 `fitz`）提取 PDF 文本
  - `python-docx` 处理 Word 文档
- 自动监控文件夹（如使用 `watchdog`）或通过 Web 上传

### 2. 元数据提取
- 标题、作者、摘要、关键词、发表年份等
- 工具：
  - `GROBID`（学术 PDF 解析神器，基于深度学习）
  - `ScienceParse`（MIT 开源）
  - 或用 LLM 提示工程从全文中抽取（如调用本地 `Llama3` 或 `Qwen`）

> 示例：用 GROBID 提取结构化信息  
> ```bash
> docker run -p 8070:8070 lfoppiano/grobid:0.8.0
> ```

### 3. 文本向量化（Embedding）
- 将论文标题+摘要+正文片段转换为向量
- 推荐模型：
  - `text-embedding-3-small`（OpenAI，需 API）
  - `BAAI/bge-large-en-v1.5` 或 `bge-m3`（开源，支持多语言，效果极佳）
  - `sentence-transformers/all-MiniLM-L6-v2`（轻量级）

> 示例（使用 HuggingFace）：
> ```python
> from sentence_transformers import SentenceTransformer
> model = SentenceTransformer('BAAI/bge-m3')
> embedding = model.encode("Your paper abstract...")
> ```

### 4. 自动分类 / 聚类
#### 方式 A：有监督分类（需标签）
- 若你有领域标签（如“计算机视觉”、“NLP”、“生物医学”）
- 用 BERT 微调分类器（`transformers` + `Trainer`）

#### 方式 B：无监督聚类（更通用）
- 对嵌入向量做聚类：
  - `KMeans`
  - `HDBSCAN`（自动确定簇数）
  - 可结合 LLM 给每个簇生成标签（如：“该簇包含关于大语言模型推理优化的论文”）

### 5. 向量数据库存储
- 推荐工具：
  - **ChromaDB**（轻量，适合本地）
  - **Qdrant**（高性能，支持过滤）
  - **Weaviate**（带图谱能力）
  - **Milvus / Zilliz**（大规模部署）

> 存储字段建议：
> - `id`, `title`, `authors`, `abstract`, `full_text_snippet`, `year`, `category`, `embedding`, `file_path`

### 6. 搜索与问答（RAG 架构）
- 用户输入自然语言查询（如“有哪些关于扩散模型加速的论文？”）
- 步骤：
  1. 对查询做相同嵌入
  2. 在向量库中做近似最近邻搜索（ANN）
  3. 返回 top-k 相关论文（含元数据）
  4. （可选）用 LLM 生成摘要或回答（RAG）

> 示例框架：
> - LangChain / LlamaIndex 构建检索链
> - 使用 `Qwen`、`Llama3`、`Phi-3` 等本地模型避免 API 成本

### 7. 用户界面（可选但推荐）
- Web 应用：Streamlit / Gradio 快速搭建
- 高级版：React + FastAPI
- 功能：
  - 上传论文
  - 按关键词/年份/类别筛选
  - 语义搜索框
  - 显示 PDF 预览（如 `pdf.js`）

---

## 三、技术栈推荐（全开源方案）

| 功能 | 工具 |
|------|------|
| PDF 解析 | GROBID + PyMuPDF |
| 嵌入模型 | BGE-M3 (HuggingFace) |
| 向量库 | ChromaDB 或 Qdrant |
| LLM（本地） | Ollama + Qwen2 / Llama3 |
| 框架 | LangChain / LlamaIndex |
| 前端 | Streamlit / Gradio |
| 部署 | Docker + FastAPI |

---

## 四、进阶功能（可选）

- **自动去重**：基于标题/DOI/嵌入相似度
- **引用关系图谱**：解析参考文献，构建知识图谱（用 `GROBID` 提取 citation）
- **定期更新**：对接 arXiv API 自动抓取新论文
- **多模态支持**：处理图表（未来方向）

---

## 五、示例项目参考

- **PaperPal**（GitHub 上多个类似项目）
- **Obsidian + Smart Connections 插件**（非代码方案）
- **Zotero + SciBERT 插件**（半自动）
- 开源项目：`semantic-scholar-agent`, `paper-organizer`

---

## 六、部署建议

- **个人使用**：本地运行（Python + Chroma + Ollama）
- **团队共享**：部署 Qdrant + FastAPI + React 前端到服务器
- **云服务**：AWS SageMaker / Google Vertex AI（适合大规模）

---

如果你希望我提供一个最小可行代码示例（比如用 Chroma + BGE + Streamlit 实现搜索），也可以告诉我，我可以直接给出完整脚本。
