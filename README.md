# PaperPilot

📚 **智能论文管理系统** - 本地运行的开源论文管理和语义搜索工具

## 🌟 功能特性

- ✅ **自动摄入 PDF 论文** - 支持单个或批量导入
- ✅ **元数据提取** - 自动提取标题、作者、年份等信息
- ✅ **向量化存储** - 使用 ChromaDB 进行高效存储
- ✅ **语义搜索** - 自然语言查询，返回最相关段落
- ✅ **Web 界面** - 基于 Streamlit 的友好交互界面
- ✅ **本地优先** - 所有数据和模型均在本地运行

## 🔧 技术栈

| 模块 | 技术选型 | 说明 |
|------|--------|------|
| 文本提取 | `pymupdf` (fitz) | 比 PyPDF2 更鲁棒，支持表格/公式保留 |
| 嵌入模型 | `BAAI/bge-m3` via `sentence-transformers` | 开源 SOTA 多语言嵌入模型 |
| 向量库 | `ChromaDB` (in-memory) | 轻量，无需部署，Python 原生支持 |
| 前端 | `Streamlit` | 快速构建 UI，简洁易用 |
| 分块策略 | 固定长度（512 字符，重叠 50） | 简单有效 |

## 📦 安装

### 1. 克隆仓库
```bash
git clone https://github.com/chisuhua/PaperPilot.git
cd PaperPilot
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

**注意**: 首次运行时会自动下载 `BAAI/bge-m3` 模型（约 2.2GB），请确保网络连接正常。

## 🚀 快速开始

### 方式 1: Web 界面（推荐）

启动 Streamlit 应用：

```bash
streamlit run app.py
```

然后在浏览器中访问 http://localhost:8501

**操作步骤**:
1. 点击侧边栏的 "🚀 初始化系统" 按钮
2. 上传 PDF 文件或指定包含 PDF 的目录
3. 在搜索框中输入自然语言查询
4. 查看相关结果和文本段落

### 方式 2: Python API

```python
from paper_manager import PaperManager

# 初始化系统
manager = PaperManager(chunk_size=512, overlap=50)

# 添加单篇论文
paper_id = manager.add_paper("path/to/paper.pdf")

# 或从目录批量添加
paper_ids = manager.add_papers_from_directory("path/to/papers/")

# 语义搜索
results = manager.search("深度学习在图像识别中的应用", n_results=5)

# 查看结果
for result in results:
    print(f"标题: {result['title']}")
    print(f"相关度: {result['relevance_score']:.2%}")
    print(f"文本: {result['text'][:200]}...")
    print("-" * 80)
```

## 📂 项目结构

```
PaperPilot/
├── app.py              # Streamlit Web 界面
├── paper_manager.py    # 主要论文管理类
├── pdf_extractor.py    # PDF 文本和元数据提取
├── text_chunker.py     # 文本分块处理
├── vector_store.py     # 向量存储和语义搜索
├── requirements.txt    # Python 依赖
├── example.py          # 使用示例
└── README.md          # 项目文档
```

## 🎯 使用场景

1. **文献综述** - 快速在大量论文中找到相关内容
2. **研究管理** - 组织和管理个人论文库
3. **知识提取** - 从论文中提取特定主题的段落
4. **学术研究** - 辅助文献阅读和引用查找

## ⚙️ 配置选项

### 分块参数
- `chunk_size`: 每个文本块的大小（默认: 512 字符）
- `overlap`: 块之间的重叠（默认: 50 字符）

### 模型选择
- 默认: `BAAI/bge-m3` (多语言支持，效果优秀)
- 可选: 其他 sentence-transformers 兼容模型

## 🔍 搜索示例

```python
# 自然语言查询示例
queries = [
    "机器学习模型的评估指标有哪些？",
    "Transformer 架构的工作原理",
    "卷积神经网络在图像分类中的应用",
    "强化学习的主要算法",
]

for query in queries:
    results = manager.search(query, n_results=3)
    # 处理结果...
```

## 📝 注意事项

1. **首次运行**: 首次运行会下载嵌入模型（约 2.2GB），需要一定时间
2. **内存使用**: ChromaDB 使用内存存储，大量论文可能占用较多内存
3. **PDF 质量**: 扫描版 PDF 可能提取效果不佳，建议使用文字版 PDF
4. **本地运行**: 所有处理都在本地完成，无需互联网连接（模型下载后）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF 处理
- [sentence-transformers](https://github.com/UKPLab/sentence-transformers) - 文本嵌入
- [ChromaDB](https://github.com/chroma-core/chroma) - 向量数据库
- [Streamlit](https://streamlit.io/) - Web 界面框架
- [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) - 嵌入模型