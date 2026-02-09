"""
PaperPilot - PDF 论文智能搜索系统
Streamlit 用户界面
"""
import streamlit as st
import tempfile
import os
import uuid
import shutil
from pdf_processor import PDFProcessor
from search_engine import SemanticSearchEngine


# 页面配置
st.set_page_config(
    page_title="PaperPilot - PDF 论文智能搜索",
    page_icon="📚",
    layout="wide"
)

# 初始化 session state
if 'processor' not in st.session_state:
    st.session_state.processor = PDFProcessor()

if 'search_engine' not in st.session_state:
    st.session_state.search_engine = None

if 'indexed' not in st.session_state:
    st.session_state.indexed = False


def main():
    st.title("📚 PaperPilot - PDF 论文智能搜索")
    st.markdown("### 使用自然语言搜索 PDF 论文内容")
    
    # 侧边栏 - 文件上传
    with st.sidebar:
        st.header("📂 上传 PDF 文件")
        uploaded_files = st.file_uploader(
            "选择一个或多个 PDF 文件",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"已选择 {len(uploaded_files)} 个文件")
            
            if st.button("🔄 处理并索引 PDF", type="primary"):
                with st.spinner("正在处理 PDF 文件..."):
                    # 清空之前的数据
                    st.session_state.processor = PDFProcessor()
                    
                    # 使用临时目录上下文管理器，自动清理
                    with tempfile.TemporaryDirectory() as temp_dir:
                        pdf_paths = []
                        
                        for uploaded_file in uploaded_files:
                            # 使用 UUID 避免文件名冲突
                            unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
                            temp_path = os.path.join(temp_dir, unique_filename)
                            with open(temp_path, 'wb') as f:
                                f.write(uploaded_file.getbuffer())
                            pdf_paths.append(temp_path)
                        
                        # 处理 PDF
                        results = st.session_state.processor.process_multiple_pdfs(pdf_paths)
                    
                    # 统计信息
                    total_paragraphs = sum(len(doc['paragraphs']) for doc in results)
                    st.success(f"✅ 处理完成！")
                    st.info(f"📄 文件数: {len(results)}")
                    st.info(f"📝 段落数: {total_paragraphs}")
                
                with st.spinner("正在建立搜索索引..."):
                    # 初始化搜索引擎
                    st.session_state.search_engine = SemanticSearchEngine()
                    
                    # 获取所有段落并建立索引
                    all_paragraphs = st.session_state.processor.get_all_paragraphs()
                    st.session_state.search_engine.index_paragraphs(all_paragraphs)
                    st.session_state.indexed = True
                    
                    st.success("✅ 索引建立完成！可以开始搜索了。")
        
        # 显示已加载的文档
        if st.session_state.processor.documents:
            st.markdown("---")
            st.subheader("已加载的文档")
            for doc_info in st.session_state.processor.documents.values():
                st.text(f"📄 {doc_info['filename']}")
    
    # 主界面 - 搜索
    if st.session_state.indexed:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input(
                "🔍 输入搜索查询",
                placeholder="例如：深度学习的应用、注意力机制、transformer 架构等..."
            )
        
        with col2:
            top_k = st.number_input(
                "返回结果数",
                min_value=1,
                max_value=20,
                value=5
            )
        
        if st.button("搜索", type="primary") and query:
            with st.spinner("搜索中..."):
                results = st.session_state.search_engine.search(query, top_k=top_k)
                
                if results:
                    st.success(f"找到 {len(results)} 个相关段落")
                    st.markdown("---")
                    
                    # 显示搜索结果
                    for i, result in enumerate(results):
                        with st.expander(
                            f"#{i+1} - {result['filename']} (相似度: {result['similarity_score']:.3f})",
                            expanded=(i < 3)  # 默认展开前3个结果
                        ):
                            st.markdown(f"**文件:** {result['filename']}")
                            st.markdown(f"**段落编号:** {result['paragraph_index'] + 1}")
                            st.markdown(f"**相似度分数:** {result['similarity_score']:.4f}")
                            st.markdown("---")
                            st.markdown("**段落内容:**")
                            st.write(result['paragraph'])
                else:
                    st.warning("未找到相关结果")
    else:
        st.info("👈 请先在左侧上传 PDF 文件并建立索引")
        
        # 使用说明
        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        1. 在左侧上传一个或多个 PDF 文件
        2. 点击"处理并索引 PDF"按钮
        3. 等待处理完成后，在搜索框中输入自然语言查询
        4. 系统将返回最相关的段落
        
        **支持的查询类型：**
        - 中文自然语言查询
        - 英文自然语言查询
        - 技术术语和关键词
        - 问题式查询（如"什么是...？"）
        """)


if __name__ == "__main__":
    main()
