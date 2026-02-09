# PaperPilot 📚

一个基于自然语言处理的 PDF 论文智能搜索系统，支持使用自然语言查询本地 PDF 文档内容。

## 界面预览

### 主界面
![PaperPilot Interface](https://github.com/user-attachments/assets/13a0d564-ac59-43f2-80dd-bfe06662bd5d)

### 搜索结果展示
![Search Results](https://github.com/user-attachments/assets/83790012-dff2-4c65-ad41-74f1de1c2fc4)

## 功能特性

- 📄 **多 PDF 支持**: 可同时加载和搜索多个 PDF 文件
- 🔍 **自然语言搜索**: 使用中文或英文进行语义搜索
- 🎯 **智能匹配**: 基于句子嵌入和余弦相似度的语义匹配
- 🌐 **多语言支持**: 支持中英文混合查询
- 💻 **友好界面**: 基于 Streamlit 的现代化 Web 界面

## 安装

### 依赖要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/chisuhua/PaperPilot.git
cd PaperPilot
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 启动应用

运行以下命令启动 Streamlit 应用：

```bash
streamlit run app.py
```

应用将在浏览器中自动打开（通常在 http://localhost:8501）

### 使用流程

1. **上传 PDF 文件**
   - 在左侧边栏点击"选择一个或多个 PDF 文件"
   - 选择要搜索的 PDF 论文
   - 可以同时上传多个文件

2. **处理和索引**
   - 点击"处理并索引 PDF"按钮
   - 系统会自动提取文本并建立搜索索引
   - 等待处理完成的提示

3. **执行搜索**
   - 在搜索框中输入自然语言查询
   - 设置返回结果数量（1-20）
   - 点击"搜索"按钮

4. **查看结果**
   - 系统会返回最相关的段落
   - 每个结果包含文件名、相似度分数和段落内容
   - 点击展开查看完整段落

### 查询示例

- "深度学习的应用"
- "注意力机制如何工作"
- "transformer 架构的优势"
- "What is neural network?"
- "机器学习算法比较"

## 项目结构

```
PaperPilot/
├── app.py              # Streamlit 应用主程序
├── pdf_processor.py    # PDF 文件处理模块
├── search_engine.py    # 语义搜索引擎模块
├── requirements.txt    # 项目依赖
└── README.md          # 项目说明
```

## 技术栈

- **Streamlit**: Web 应用框架
- **PyPDF2**: PDF 文本提取
- **Sentence Transformers**: 句子嵌入模型
- **scikit-learn**: 相似度计算
- **PyTorch**: 深度学习框架

## 核心模块说明

### pdf_processor.py
负责 PDF 文件的处理和文本提取：
- 提取 PDF 文本内容
- 将文本分割成段落
- 管理多个文档

### search_engine.py
实现语义搜索功能：
- 加载预训练的多语言句子嵌入模型
- 为文档段落建立索引
- 执行自然语言查询并返回相关结果

### app.py
提供 Streamlit 用户界面：
- 文件上传和管理
- 搜索界面
- 结果展示

## 注意事项

- 首次运行时会自动下载语言模型，可能需要一些时间
- 建议使用 PDF 文本版文件（而非扫描版）以获得更好的效果
- 处理大量 PDF 文件时可能需要较长时间

## License

MIT License - 详见 LICENSE 文件

## 贡献

欢迎提交 Issue 和 Pull Request！