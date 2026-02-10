# PaperPilot 快速开始指南

本文档提供 PaperPilot 的快速安装和使用说明。

## 📦 安装方式

### 方式 1: 从源码安装（开发者推荐）

```bash
# 克隆仓库
git clone https://github.com/chisuhua/PaperPilot.git
cd PaperPilot

# 安装依赖
pip install -r requirements.txt

# 验证安装
python verify_structure.py
```

### 方式 2: 使用 pip 安装（推荐）

```bash
# 从源码目录安装
pip install -e .

# 或者直接从 GitHub 安装
pip install git+https://github.com/chisuhua/PaperPilot.git
```

## 🚀 快速使用

### 1. Web 界面使用

启动 Streamlit 应用：

```bash
streamlit run paperpilot/ui/app.py
```

访问 http://localhost:8501 查看界面。

### 2. Python API 使用

```python
from paperpilot import PaperManager

# 初始化管理器
manager = PaperManager()

# 添加论文
paper_id = manager.add_paper("path/to/paper.pdf")

# 搜索
results = manager.search("深度学习", n_results=5)

# 查看结果
for result in results:
    print(f"{result['title']}: {result['relevance_score']:.2%}")
```

### 3. 命令行使用示例

```bash
# 运行基础演示
python examples/demo.py

# 运行完整示例
python examples/example.py

# 运行测试
python tests/test_components.py
```

## 📂 项目结构说明

```
PaperPilot/
├── paperpilot/              # 主包
│   ├── core/               # 核心功能模块
│   │   ├── pdf_extractor.py     # PDF 提取
│   │   ├── text_chunker.py      # 文本分块
│   │   ├── vector_store.py      # 向量存储
│   │   ├── paper_manager.py     # 论文管理
│   │   └── search_engine.py     # 搜索引擎
│   └── ui/                 # 用户界面
│       ├── app.py          # 主应用
│       └── app_demo.py     # 演示版
├── examples/               # 使用示例
├── tests/                  # 测试文件
├── docs/                   # 详细文档
└── config.yaml            # 配置文件
```

## ⚙️ 配置说明

编辑 `config.yaml` 自定义配置：

```yaml
# 模型配置
model:
  name: "BAAI/bge-m3"
  cache_dir: "./models"

# 分块配置
chunking:
  chunk_size: 512
  overlap: 50

# 数据库配置
chromadb:
  persist_directory: "./chroma_db"
  collection_name: "papers"
```

## 🔍 常见问题

### Q: 首次运行很慢？
A: 首次运行需要下载 2.2GB 的嵌入模型，请耐心等待。

### Q: 如何处理多个 PDF？
A: 使用 `add_papers_from_directory()` 方法批量添加。

### Q: 支持哪些语言？
A: 支持中文和英文，使用多语言模型 bge-m3。

### Q: 数据存储在哪里？
A: 默认存储在 `./chroma_db/` 目录，可在配置文件中修改。

## 📖 更多文档

- **[详细使用说明](docs/USAGE.md)** - 完整使用指南
- **[架构文档](docs/PLAN.md)** - 技术架构说明
- **[API 文档](docs/API.md)** - API 参考（待补充）

## 🆘 获取帮助

- 查看 [GitHub Issues](https://github.com/chisuhua/PaperPilot/issues)
- 阅读项目 [README.md](../README.md)
- 参考 [示例代码](../examples/)

## 📝 下一步

1. 阅读 [USAGE.md](docs/USAGE.md) 了解详细用法
2. 查看 [examples/](../examples/) 学习示例代码
3. 根据需要修改 `config.yaml` 配置
4. 开始使用 PaperPilot 管理您的论文库！
