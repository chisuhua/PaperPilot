"""
Example usage of PaperPilot system.
Demonstrates basic functionality without the web interface.
"""

from paperpilot.core import PaperManager
from pathlib import Path


def main():
    print("=" * 80)
    print("PaperPilot - 智能论文管理系统示例")
    print("=" * 80)
    
    # Initialize the system
    print("\n1. 初始化系统...")
    manager = PaperManager(
        chunk_size=512,
        overlap=50,
        model_name="BAAI/bge-m3"
    )
    print("✓ 系统初始化完成")
    
    # Example: Add papers from a directory
    print("\n2. 添加论文...")
    print("提示: 请将PDF文件放在papers/目录下")
    
    papers_dir = Path("papers")
    if papers_dir.exists():
        paper_ids = manager.add_papers_from_directory("papers")
        if paper_ids:
            print(f"✓ 成功加载 {len(paper_ids)} 篇论文")
        else:
            print("! 未找到PDF文件，将使用示例查询")
    else:
        print(f"! papers/目录不存在，将创建示例目录")
        papers_dir.mkdir(exist_ok=True)
        print(f"  请将PDF文件放入 {papers_dir.absolute()} 目录，然后重新运行")
    
    # Get statistics
    print("\n3. 系统统计信息...")
    stats = manager.get_stats()
    print(f"  - 论文总数: {stats['total_papers']}")
    print(f"  - 文本块总数: {stats['total_chunks']}")
    
    if stats['total_papers'] > 0:
        print("\n  已加载的论文:")
        for paper in stats['papers']:
            print(f"    • {paper['title']}")
            print(f"      作者: {paper['author']}, 年份: {paper['year'] or 'N/A'}, 页数: {paper['pages']}")
    
    # Example searches (only if papers are loaded)
    if stats['total_papers'] > 0:
        print("\n4. 语义搜索示例...")
        
        # Example queries
        example_queries = [
            "深度学习的基本原理",
            "神经网络的训练方法",
            "机器学习的应用场景",
        ]
        
        print("\n尝试以下查询，或输入自定义查询 (输入q退出):")
        for i, q in enumerate(example_queries, 1):
            print(f"  {i}. {q}")
        
        while True:
            print("\n" + "-" * 80)
            user_input = input("\n输入查询 (或输入1-3选择示例查询，q退出): ").strip()
            
            if user_input.lower() == 'q':
                break
            
            # Check if user selected an example query
            if user_input.isdigit() and 1 <= int(user_input) <= len(example_queries):
                query = example_queries[int(user_input) - 1]
            else:
                query = user_input
            
            if not query:
                continue
            
            print(f"\n🔍 搜索: {query}")
            results = manager.search(query, n_results=3)
            
            print(f"\n找到 {len(results)} 个相关结果:\n")
            
            for i, result in enumerate(results, 1):
                print(f"{'=' * 80}")
                print(f"结果 {i}:")
                print(f"  标题: {result['title']}")
                print(f"  作者: {result['author']}")
                print(f"  年份: {result['year'] or 'N/A'}")
                print(f"  相关度: {result['relevance_score']:.2%}")
                print(f"\n  相关文本:")
                print(f"  {'-' * 76}")
                # Print first 300 characters of the text
                text_preview = result['text'][:300]
                if len(result['text']) > 300:
                    text_preview += "..."
                print(f"  {text_preview}")
                print()
    else:
        print("\n提示: 添加PDF论文后可以进行语义搜索")
    
    print("\n" + "=" * 80)
    print("示例结束")
    print("\n建议使用 Web 界面获得更好的体验:")
    print("  streamlit run app.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
