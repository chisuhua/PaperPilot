#!/usr/bin/env python3
"""
Demo script showing PaperPilot functionality
演示 PaperPilot 功能的脚本
"""


def main() -> None:
    """Main demo function"""
    print("=" * 80)
    print("PaperPilot - PDF 论文智能搜索系统演示")
    print("=" * 80)

    print("\n1. 导入模块...")
    from pdf_processor import PDFProcessor
    print("   ✓ PDF 处理模块已加载")

    print("\n2. 初始化 PDF 处理器...")
    processor = PDFProcessor()
    print("   ✓ 处理器初始化完成")

    print("\n3. 处理示例 PDF 文件...")
    import os
    pdf_path = "/tmp/test_pdfs/sample_paper.pdf"
    if os.path.exists(pdf_path):
        doc_info = processor.process_pdf(pdf_path)
        print(f"   ✓ PDF 处理完成: {doc_info['filename']}")
        print(f"   ✓ 提取段落数: {len(doc_info['paragraphs'])}")
        
        print("\n4. 文档内容预览:")
        print("-" * 80)
        for i, para in enumerate(doc_info['paragraphs'][:2]):  # Show first 2 paragraphs
            print(f"\n   段落 {i+1}:")
            preview = para[:200] + "..." if len(para) > 200 else para
            print(f"   {preview}")
        print("-" * 80)
        
        print("\n5. 获取所有段落...")
        all_paragraphs = processor.get_all_paragraphs()
        print(f"   ✓ 总段落数: {len(all_paragraphs)}")
        
        print("\n✅ 演示完成!")
        print("\n说明:")
        print("  - PDF 文本提取功能正常工作")
        print("  - 段落分割功能正常工作")
        print("  - 多文档管理功能正常工作")
        print("\n完整功能需要安装所有依赖:")
        print("  pip install -r requirements.txt")
        print("\n启动 Streamlit 应用:")
        print("  streamlit run app.py")
    else:
        print(f"   ✗ 未找到示例 PDF: {pdf_path}")
        print("   请先在该路径下放置一个名为 sample_paper.pdf 的示例 PDF 文件后重试。")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
