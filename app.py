"""
<<<<<<< HEAD
<<<<<<< HEAD
PaperPilot - PDF 论文智能搜索系统 (V2)
基于 PLAN.md 架构：pymupdf + bge-m3 + ChromaDB
"""
import streamlit as st
import tempfile
import os
import uuid
import yaml
import logging
from pathlib import Path

from paper_manager import PaperManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载配置
try:
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    logger.warning("config.yaml not found, using defaults")
    config = {
        'ui': {
            'page_title': 'PaperPilot - PDF 论文智能搜索',
            'page_icon': '📚',
            'layout': 'wide',
            'default_top_k': 5,
            'max_top_k': 20
        }
    }

# 页面配置
st.set_page_config(
    page_title=config['ui']['page_title'],
    page_icon=config['ui']['page_icon'],
    layout=config['ui']['layout']
)

# 初始化 PaperManager（使用 session state 保持状态）
if 'manager' not in st.session_state:
    with st.spinner("正在加载模型..."):
        try:
            st.session_state.manager = PaperManager()
            st.session_state.initialized = True
            logger.info("PaperManager initialized successfully")
        except Exception as e:
            st.error(f"初始化失败: {e}")
            st.session_state.initialized = False
            st.stop()


def main():
    st.title("📚 PaperPilot - PDF 论文智能搜索 V2")
    st.markdown("### 🚀 基于 PLAN.md 架构 (pymupdf + bge-m3 + ChromaDB)")
    
    # 显示系统统计
    with st.sidebar:
        st.header("📊 系统状态")
        
        if st.session_state.initialized:
            stats = st.session_state.manager.get_stats()
            st.metric("已索引块数", stats['total_chunks'])
            st.metric("嵌入模型", stats['model_name'])
            
            with st.expander("详细配置"):
                st.write(f"**分块大小**: {stats['chunk_size']} 字符")
                st.write(f"**重叠大小**: {stats['chunk_overlap']} 字符")
                st.write(f"**集合名称**: {stats['collection_name']}")
        
        st.markdown("---")
        st.header("📂 上传 PDF 文件")
        
        uploaded_files = st.file_uploader(
            "选择一个或多个 PDF 文件",
            type=['pdf'],
            accept_multiple_files=True,
            key="pdf_uploader"
        )
        
        if uploaded_files:
            st.success(f"已选择 {len(uploaded_files)} 个文件")
            
            if st.button("🔄 处理并索引 PDF", type="primary"):
                process_pdfs(uploaded_files)
        
        st.markdown("---")
        
        # 重置按钮
        if st.button("🗑️ 清空所有数据", type="secondary"):
            if st.session_state.initialized:
                st.session_state.manager.reset()
                st.success("数据已清空！")
                st.rerun()
    
    # 主界面 - 搜索
    if st.session_state.initialized:
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input(
                "🔍 输入搜索查询",
                placeholder="例如：深度学习的应用、注意力机制、transformer 架构...",
                key="search_query"
            )
        
        with col2:
            top_k = st.number_input(
                "返回结果数",
                min_value=1,
                max_value=config['ui']['max_top_k'],
                value=config['ui']['default_top_k'],
                key="top_k"
            )
        
        # 高级过滤选项
        with st.expander("🔧 高级过滤"):
            col1, col2 = st.columns(2)
            with col1:
                year_filter = st.text_input("年份", placeholder="例如: 2024")
            with col2:
                title_filter = st.text_input("标题关键词", placeholder="例如: transformer")
        
        if st.button("搜索", type="primary", key="search_button") and query:
            perform_search(query, top_k, year_filter, title_filter)
        
        # 显示使用提示
        if not query:
            st.markdown("---")
            show_usage_guide()


def process_pdfs(uploaded_files):
    """处理上传的 PDF 文件"""
    with st.spinner(f"正在处理 {len(uploaded_files)} 个 PDF 文件..."):
        # 使用临时目录保存文件
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_paths = []
            
            for uploaded_file in uploaded_files:
                # 使用 UUID 避免文件名冲突
                unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
                temp_path = os.path.join(temp_dir, unique_filename)
                
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                pdf_paths.append(temp_path)
            
            # 批量处理
            results = st.session_state.manager.add_papers_batch(
                pdf_paths,
                show_progress=False
            )
        
        # 显示结果
        st.success(f"✅ 处理完成！")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("成功", results['successful'])
        with col2:
            st.metric("失败", results['failed'])
        with col3:
            st.metric("新增块数", results['total_chunks'])
        
        # 显示详细结果
        if results['failed'] > 0:
            with st.expander("查看失败详情"):
                for detail in results['details']:
                    if not detail['success']:
                        st.error(f"❌ {Path(detail['pdf_path']).name}: {detail['error']}")


def perform_search(query: str, top_k: int, year_filter: str = "", title_filter: str = ""):
    """执行搜索"""
    with st.spinner("搜索中..."):
        # 构建过滤器
        filters = None
        if year_filter:
            try:
                filters = {"year": int(year_filter)}
            except ValueError:
                st.warning("年份格式无效，已忽略")
        
        # 执行搜索
        results = st.session_state.manager.search(
            query=query,
            top_k=top_k,
            filters=filters
        )
    
    if results:
        st.success(f"找到 {len(results)} 个相关结果")
        st.markdown("---")
        
        # 显示搜索结果
        for i, result in enumerate(results):
            metadata = result['metadata']
            
            # 标题和元数据
            title = metadata.get('title', '未知标题')
            filename = metadata.get('filename', '未知文件')
            year = metadata.get('year', '')
            chunk_index = metadata.get('chunk_index', 0)
            
            # 相似度分数
            similarity = result['similarity_score']
            
            # 使用 expander 显示结果
            with st.expander(
                f"#{i+1} - {title} ({year}) - 相似度: {similarity:.3f}",
                expanded=(i < 3)  # 默认展开前3个结果
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**文件**: {filename}")
                    st.markdown(f"**标题**: {title}")
                    if year:
                        st.markdown(f"**年份**: {year}")
                
                with col2:
                    st.metric("相似度分数", f"{similarity:.4f}")
                    st.markdown(f"**块索引**: {chunk_index}")
                
                st.markdown("---")
                st.markdown("**内容预览**:")
                st.write(result['document'])
    else:
        st.warning("未找到相关结果")


def show_usage_guide():
    """显示使用指南"""
    st.markdown("### 📖 使用指南")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🚀 快速开始
        
        1. **上传 PDF**
           - 点击左侧「上传 PDF 文件」
           - 选择一个或多个 PDF
           - 点击「处理并索引 PDF」
        
        2. **搜索论文**
           - 在搜索框输入自然语言查询
           - 设置返回结果数量
           - 点击「搜索」按钮
        
        3. **查看结果**
           - 结果按相似度排序
           - 点击展开查看完整内容
           - 使用高级过滤缩小范围
        """)
    
    with col2:
        st.markdown("""
        #### ✨ V2 新特性
        
        - ✅ **持久化存储**
          数据永久保存，重启不丢失
        
        - ✅ **增量索引**
          新文档秒级添加，无需重建
        
        - ✅ **更高准确率**
          bge-m3 模型，搜索准确率 ~85%
        
        - ✅ **元数据支持**
          自动提取标题、年份等信息
        
        - ✅ **高级过滤**
          按年份、标题等条件筛选
        """)
    
    st.markdown("---")
    st.info("""
    💡 **提示**：首次运行会下载 bge-m3 模型（约 2.2GB），请耐心等待。
    数据存储在 `./chroma_db` 目录，可以随时备份。
    """)


if __name__ == "__main__":
    main()
=======
=======
>>>>>>> c82a479dad18df57429f18f3673a14377b64e1d2
Streamlit web interface for PaperPilot.
Provides an interactive UI for paper management and semantic search.
"""

import streamlit as st
from pathlib import Path
from paper_manager import PaperManager
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="PaperPilot - 智能论文管理系统",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'manager' not in st.session_state:
    st.session_state.manager = None
if 'papers_loaded' not in st.session_state:
    st.session_state.papers_loaded = False

# Title and description
st.title("📚 PaperPilot - 智能论文管理系统")
st.markdown("""
本地运行的智能论文管理系统，支持PDF论文的自动摄入、元数据提取、向量化存储和语义搜索。

**技术栈**: PyMuPDF + BAAI/bge-m3 + ChromaDB + Streamlit
""")

# Sidebar for configuration and paper loading
with st.sidebar:
    st.header("⚙️ 配置")
    
    # Model configuration
    with st.expander("模型设置", expanded=False):
        chunk_size = st.number_input("块大小 (字符)", value=512, min_value=100, max_value=2000)
        overlap = st.number_input("重叠大小 (字符)", value=50, min_value=0, max_value=500)
        model_name = st.text_input("嵌入模型", value="BAAI/bge-m3")
    
    # Initialize system
    if st.button("🚀 初始化系统", type="primary"):
        with st.spinner("正在初始化系统和加载模型..."):
            try:
                st.session_state.manager = PaperManager(
                    chunk_size=chunk_size,
                    overlap=overlap,
                    model_name=model_name
                )
                st.success("系统初始化成功！")
            except Exception as e:
                st.error(f"初始化失败: {e}")
    
    st.divider()
    
    # Paper loading
    st.header("📥 加载论文")
    
    # Upload PDFs
    uploaded_files = st.file_uploader(
        "上传 PDF 文件",
        type=['pdf'],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.session_state.manager:
        if st.button("处理上传的文件"):
            with st.spinner("正在处理PDF文件..."):
                # Create temporary directory for uploads
                temp_dir = Path(tempfile.gettempdir()) / "paperpilot_uploads"
                temp_dir.mkdir(exist_ok=True)
                
                paper_ids = []
                for uploaded_file in uploaded_files:
                    # Save uploaded file temporarily
                    temp_path = temp_dir / uploaded_file.name
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.read())
                    
                    try:
                        paper_id = st.session_state.manager.add_paper(str(temp_path))
                        paper_ids.append(paper_id)
                    except Exception as e:
                        st.error(f"处理 {uploaded_file.name} 失败: {e}")
                
                if paper_ids:
                    st.session_state.papers_loaded = True
                    st.success(f"成功加载 {len(paper_ids)} 篇论文！")
    
    # Load from directory
    st.markdown("**或从目录加载**")
    directory_path = st.text_input("PDF 目录路径", value="")
    
    if directory_path and st.session_state.manager:
        if st.button("从目录加载"):
            with st.spinner("正在加载论文..."):
                try:
                    paper_ids = st.session_state.manager.add_papers_from_directory(directory_path)
                    if paper_ids:
                        st.session_state.papers_loaded = True
                        st.success(f"成功加载 {len(paper_ids)} 篇论文！")
                except Exception as e:
                    st.error(f"加载失败: {e}")

# Main content area
if st.session_state.manager is None:
    st.info("👈 请先在侧边栏初始化系统")
else:
    # Display statistics
    stats = st.session_state.manager.get_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("论文总数", stats['total_papers'])
    with col2:
        st.metric("文本块总数", stats['total_chunks'])
    with col3:
        avg_chunks = stats['total_chunks'] / stats['total_papers'] if stats['total_papers'] > 0 else 0
        st.metric("平均块数/论文", f"{avg_chunks:.0f}")
    
    # Show loaded papers
    if stats['total_papers'] > 0:
        with st.expander("📋 已加载的论文", expanded=False):
            for paper in stats['papers']:
                st.markdown(f"""
                - **{paper['title']}** 
                  - 作者: {paper['author']} 
                  - 年份: {paper['year'] or 'N/A'}
                  - 页数: {paper['pages']}
                  - 文件: {paper['filename']}
                """)
    
    st.divider()
    
    # Search interface
    st.header("🔍 语义搜索")
    
    if not st.session_state.papers_loaded:
        st.warning("请先上传或加载论文")
    else:
        # Search query
        query = st.text_input(
            "输入搜索查询 (自然语言)",
            placeholder="例如: 深度学习在图像识别中的应用",
            help="使用自然语言描述您要查找的内容"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            n_results = st.slider("返回结果数量", min_value=1, max_value=20, value=5)
        with col2:
            search_button = st.button("🔎 搜索", type="primary", use_container_width=True)
        
        # Perform search
        if search_button and query:
            with st.spinner("正在搜索..."):
                try:
                    results = st.session_state.manager.search(query, n_results=n_results)
                    
                    st.subheader(f"找到 {len(results)} 个相关结果")
                    
                    # Display results
                    for i, result in enumerate(results, 1):
                        with st.expander(
                            f"结果 {i}: {result['title']} (相关度: {result['relevance_score']:.2%})",
                            expanded=(i == 1)
                        ):
                            st.markdown(f"**论文信息:**")
                            st.markdown(f"- 标题: {result['title']}")
                            st.markdown(f"- 作者: {result['author']}")
                            st.markdown(f"- 年份: {result['year'] or 'N/A'}")
                            st.markdown(f"- 文件: {result['filename']}")
                            st.markdown(f"- 文本块索引: {result['chunk_index']}")
                            
                            st.markdown("**相关文本:**")
                            st.text_area(
                                "内容",
                                value=result['text'],
                                height=200,
                                key=f"result_{i}",
                                label_visibility="collapsed"
                            )
                
                except Exception as e:
                    st.error(f"搜索出错: {e}")
        
        elif search_button and not query:
            st.warning("请输入搜索查询")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    PaperPilot - 开源本地论文管理系统 | 技术栈: PyMuPDF + BAAI/bge-m3 + ChromaDB + Streamlit
</div>
""", unsafe_allow_html=True)
<<<<<<< HEAD
>>>>>>> c82a479
=======
>>>>>>> c82a479dad18df57429f18f3673a14377b64e1d2
