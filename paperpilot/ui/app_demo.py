"""
PaperPilot - PDF 论文智能搜索系统（演示版本）
Streamlit 用户界面 - 不需要完整依赖的演示版
"""
import streamlit as st

# 页面配置
st.set_page_config(
    page_title="PaperPilot - PDF 论文智能搜索",
    page_icon="📚",
    layout="wide"
)

def main():
    st.title("📚 PaperPilot - PDF 论文智能搜索")
    st.markdown("### 使用自然语言搜索 PDF 论文内容")
    
    # 侧边栏 - 文件上传
    with st.sidebar:
        st.header("📂 上传 PDF 文件")
        
        st.markdown("""
        **功能演示版本**
        
        完整功能包括：
        - ✅ 支持单个或多个 PDF 文件上传
        - ✅ 自动提取文本和段落
        - ✅ 语义搜索索引构建
        - ✅ 自然语言查询（中英文）
        - ✅ 智能段落匹配和排序
        
        要运行完整版本，请安装：
        """)
        
        st.code("pip install -r requirements.txt", language="bash")
        
        st.markdown("---")
        st.markdown("### 📦 已实现的模块")
        st.markdown("""
        - `pdf_processor.py` - PDF 处理
        - `search_engine.py` - 语义搜索
        - `app.py` - Streamlit 界面
        """)
    
    # 主界面
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🔍 搜索演示")
        
        query = st.text_input(
            "输入搜索查询",
            placeholder="例如：深度学习的应用、注意力机制、transformer 架构等..."
        )
    
    with col2:
        top_k = st.number_input(
            "返回结果数",
            min_value=1,
            max_value=20,
            value=5
        )
    
    # 演示搜索结果
    if query:
        st.markdown("---")
        st.success(f"演示：搜索 \"{query}\" 的结果")
        
        # 模拟搜索结果
        demo_results = [
            {
                'filename': 'deep_learning_paper.pdf',
                'paragraph': 'Deep learning is a subset of machine learning that uses neural networks with multiple layers. These networks can learn complex patterns from data and have achieved remarkable success in various domains including computer vision, natural language processing, and speech recognition.',
                'paragraph_index': 0,
                'similarity_score': 0.85
            },
            {
                'filename': 'transformer_architecture.pdf',
                'paragraph': 'The attention mechanism has revolutionized the field of deep learning by allowing models to focus on relevant parts of the input. This mechanism is particularly effective in sequence-to-sequence tasks and has been widely adopted in transformer architectures.',
                'paragraph_index': 2,
                'similarity_score': 0.78
            },
            {
                'filename': 'neural_networks.pdf',
                'paragraph': 'Neural networks are computational models inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers. Each connection has an associated weight that is adjusted during training to minimize the error between predicted and actual outputs.',
                'paragraph_index': 1,
                'similarity_score': 0.72
            }
        ]
        
        st.markdown(f"找到 {len(demo_results)} 个相关段落（演示数据）")
        
        for i, result in enumerate(demo_results):
            with st.expander(
                f"#{i+1} - {result['filename']} (相似度: {result['similarity_score']:.3f})",
                expanded=(i < 2)
            ):
                st.markdown(f"**文件:** {result['filename']}")
                st.markdown(f"**段落编号:** {result['paragraph_index'] + 1}")
                st.markdown(f"**相似度分数:** {result['similarity_score']:.4f}")
                st.markdown("---")
                st.markdown("**段落内容:**")
                st.write(result['paragraph'])
    
    else:
        # 使用说明
        st.markdown("---")
        st.markdown("### 📖 使用说明")
        st.markdown("""
        **这是演示版本，展示了完整的 UI 功能**
        
        完整版本使用步骤：
        1. 在左侧上传一个或多个 PDF 文件
        2. 点击"处理并索引 PDF"按钮
        3. 等待处理完成后，在搜索框中输入自然语言查询
        4. 系统将返回最相关的段落
        
        **核心技术：**
        - **PDF 处理**: PyPDF2 提取文本
        - **语义搜索**: Sentence Transformers (多语言模型)
        - **相似度计算**: 余弦相似度匹配
        - **用户界面**: Streamlit 框架
        
        **支持的查询类型：**
        - ✅ 中文自然语言查询
        - ✅ 英文自然语言查询
        - ✅ 技术术语和关键词
        - ✅ 问题式查询（如"什么是...？"）
        """)
        
        st.markdown("---")
        st.markdown("### 🚀 安装完整版本")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**安装依赖：**")
            st.code("""
pip install -r requirements.txt
            """, language="bash")
        
        with col2:
            st.markdown("**运行应用：**")
            st.code("""
streamlit run app.py
            """, language="bash")
        
        st.markdown("---")
        st.info("💡 提示：首次运行时会自动下载多语言模型（约 420MB），需要稍等片刻。")


if __name__ == "__main__":
    main()
