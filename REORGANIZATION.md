# 项目结构重组说明

## 📋 概述

本次重组旨在为 PaperPilot 项目提供更清晰、更专业的文件组织结构，便于后续开发和维护。

## 🔄 重组前后对比

### 重组前（扁平结构）

```
PaperPilot/
├── __init__.py
├── app.py
├── app_demo.py
├── paper_manager.py
├── pdf_extractor.py
├── pdf_processor.py           # 重复功能
├── search_engine.py
├── text_chunker.py
├── vector_store.py
├── demo.py
├── example.py
├── test_components.py
├── create_test_pdf.py
├── ARCHITECTURE_COMPARISON.md
├── MIGRATION_GUIDE.md
├── PLAN.md
├── RECOMMENDATION.md
├── USAGE.md
├── README.md
├── config.yaml
└── requirements.txt
```

**问题**：
- ❌ 所有文件混在根目录，难以导航
- ❌ 核心模块、示例、测试混杂
- ❌ 文档分散，不易查找
- ❌ 存在冗余文件（pdf_processor.py）
- ❌ 不符合 Python 包的标准结构

### 重组后（模块化结构）

```
PaperPilot/
├── paperpilot/              # 📦 核心包
│   ├── __init__.py         # 包入口，导出公共 API
│   ├── core/               # 🔧 核心功能模块
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py     # PDF 文本提取
│   │   ├── text_chunker.py      # 文本分块
│   │   ├── vector_store.py      # 向量存储
│   │   ├── paper_manager.py     # 论文管理（高层 API）
│   │   └── search_engine.py     # 搜索引擎
│   └── ui/                 # 🖥️ 用户界面
│       ├── __init__.py
│       ├── app.py          # Streamlit 主应用
│       └── app_demo.py     # 演示版 UI
├── examples/               # 📝 示例代码
│   ├── demo.py            # 基础功能演示
│   └── example.py         # API 使用示例
├── tests/                  # 🧪 测试文件
│   ├── test_components.py # 组件测试
│   └── create_test_pdf.py # 测试数据生成
├── docs/                   # 📚 项目文档
│   ├── ARCHITECTURE_COMPARISON.md  # 架构对比
│   ├── MIGRATION_GUIDE.md         # 迁移指南
│   ├── PLAN.md                    # 开发计划
│   ├── RECOMMENDATION.md          # 架构建议
│   └── USAGE.md                   # 详细使用说明
├── config.yaml            # ⚙️ 配置文件
├── requirements.txt       # 📋 依赖清单
├── setup.py              # 📦 包安装脚本
├── MANIFEST.in           # 📦 打包清单
├── verify_structure.py   # ✅ 结构验证脚本
├── QUICKSTART.md         # 🚀 快速开始指南
├── README.md             # 📖 项目说明
└── LICENSE               # 📄 许可证
```

**优势**：
- ✅ 清晰的模块划分，便于理解和维护
- ✅ 核心功能集中在 `paperpilot/core/`
- ✅ 示例、测试、文档分别归档
- ✅ 符合 Python 包的标准结构
- ✅ 支持 `pip install` 安装
- ✅ 便于版本发布和分发

## 📦 主要改动

### 1. 创建核心包结构

```python
paperpilot/
├── __init__.py          # 导出：PaperManager, PDFExtractor, TextChunker, VectorStore
└── core/
    ├── __init__.py      # 导出所有核心模块
    ├── pdf_extractor.py
    ├── text_chunker.py
    ├── vector_store.py
    ├── paper_manager.py
    └── search_engine.py
```

**导入方式**：
```python
# 之前（扁平导入）
from paper_manager import PaperManager
from pdf_extractor import PDFExtractor

# 之后（包导入）
from paperpilot import PaperManager, PDFExtractor
# 或
from paperpilot.core import PaperManager, PDFExtractor
```

### 2. 分离用户界面

```python
paperpilot/ui/
├── __init__.py
├── app.py          # 主 Streamlit 应用
└── app_demo.py     # 演示版
```

**启动方式**：
```bash
# 之前
streamlit run app.py

# 之后
streamlit run paperpilot/ui/app.py
```

### 3. 归档示例和测试

```
examples/          # 所有示例代码
tests/            # 所有测试文件
```

### 4. 集中项目文档

```
docs/             # 所有 Markdown 文档
├── ARCHITECTURE_COMPARISON.md
├── MIGRATION_GUIDE.md
├── PLAN.md
├── RECOMMENDATION.md
└── USAGE.md
```

### 5. 添加标准 Python 包文件

- `setup.py` - 支持 `pip install`
- `MANIFEST.in` - 包分发清单
- `verify_structure.py` - 结构验证工具
- `QUICKSTART.md` - 快速开始指南

### 6. 更新所有导入语句

所有文件的导入语句已更新为使用新的包结构：

**核心模块间**（使用相对导入）：
```python
# paper_manager.py
from .pdf_extractor import PDFExtractor
from .text_chunker import TextChunker
from .vector_store import VectorStore
```

**外部使用**（使用包导入）：
```python
# app.py, examples/*.py, tests/*.py
from paperpilot.core import PaperManager, PDFExtractor
# 或
from paperpilot import PaperManager
```

### 7. 清理冗余文件

- 删除 `pdf_processor.py`（功能由 `pdf_extractor.py` 提供）
- 清理 `.gitignore` 冲突标记
- 解决所有源文件中的 Git 合并冲突

## 🎯 使用指南

### 开发安装

```bash
# 克隆仓库
git clone https://github.com/chisuhua/PaperPilot.git
cd PaperPilot

# 安装依赖
pip install -r requirements.txt

# 以开发模式安装包
pip install -e .

# 验证结构
python verify_structure.py
```

### 用户安装

```bash
# 直接从 GitHub 安装
pip install git+https://github.com/chisuhua/PaperPilot.git
```

### 导入使用

```python
# 方式 1：从主包导入
from paperpilot import PaperManager

# 方式 2：从子模块导入
from paperpilot.core import PaperManager, PDFExtractor
from paperpilot.core import TextChunker, VectorStore

# 初始化
manager = PaperManager()
```

### 运行应用

```bash
# Web 界面
streamlit run paperpilot/ui/app.py

# 演示脚本
python examples/demo.py
python examples/example.py

# 测试
python tests/test_components.py
```

## 📊 文件统计

| 类别 | 文件数 | 说明 |
|------|--------|------|
| 核心模块 | 5 | pdf_extractor, text_chunker, vector_store, paper_manager, search_engine |
| UI 模块 | 2 | app.py, app_demo.py |
| 示例 | 2 | demo.py, example.py |
| 测试 | 2 | test_components.py, create_test_pdf.py |
| 文档 | 5 | 架构、计划、使用等文档 |
| 配置 | 4 | config.yaml, requirements.txt, setup.py, MANIFEST.in |
| 其他 | 4 | README.md, QUICKSTART.md, verify_structure.py, LICENSE |

**总计**：24 个主要文件，7 个目录

## ✅ 验证清单

- [x] 所有文件已移动到正确位置
- [x] 所有导入语句已更新
- [x] 创建了完整的 `__init__.py` 文件
- [x] 清理了冗余和冲突文件
- [x] 添加了 `setup.py` 支持包安装
- [x] 创建了结构验证脚本
- [x] 更新了 README.md
- [x] 创建了 QUICKSTART.md
- [x] 测试文件可正常运行
- [x] 符合 Python 包规范

## 🚀 下一步

1. **安装依赖**：`pip install -r requirements.txt`
2. **验证结构**：`python verify_structure.py`
3. **运行测试**：`python tests/test_components.py`
4. **启动应用**：`streamlit run paperpilot/ui/app.py`

## 📝 注意事项

1. **导入变化**：如果有外部代码引用了旧的导入路径，需要更新
2. **启动路径**：Streamlit 应用启动路径已变更
3. **包安装**：现在支持使用 `pip install -e .` 安装
4. **文档位置**：所有文档已移至 `docs/` 目录

## 🤝 贡献指南

- 核心功能代码放在 `paperpilot/core/`
- UI 相关代码放在 `paperpilot/ui/`
- 示例代码放在 `examples/`
- 测试代码放在 `tests/`
- 文档放在 `docs/`

---

**重组完成时间**：2026-02-10
**Git 分支**：`copilot/reorganize-file-paths`
