"""
Streamlit web interface for PaperPilot.
Provides an interactive UI for paper management and semantic search.
"""

import streamlit as st
from pathlib import Path
from paper_manager import PaperManager
import os

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
                temp_dir = Path("/tmp/paperpilot_uploads")
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
