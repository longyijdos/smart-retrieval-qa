"""
检索系统初始化模块
用于初始化文本检索功能
"""

import os
import sys

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ref.retrive import initialize_retriever, get_retriever


def init_retrieval_system(ref_file_path=None):
    """
    初始化检索系统
    
    Args:
        ref_file_path: 参考文档路径，如果为None则使用默认路径
    
    Returns:
        TextRetriever: 检索器实例
    """
    if ref_file_path is None:
        ref_file_path = os.path.join(current_dir, 'ref.txt')
    
    print(f"正在初始化检索系统，使用文档: {ref_file_path}")
    
    try:
        retriever = initialize_retriever(ref_file_path)
        print("检索系统初始化成功！")
        return retriever
    except Exception as e:
        print(f"检索系统初始化失败: {e}")
        return None


def test_retrieval_system():
    """测试检索系统"""
    retriever = get_retriever()
    if retriever is None:
        print("检索系统未初始化")
        return
    
    # 测试查询
    test_queries = [
        "什么是大语言模型",
        "GPT-4的特点",
        "大语言模型的应用",
        "强化学习"
    ]
    
    print("=" * 50)
    print("检索系统测试")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\n查询: {query}")
        print("-" * 30)
        context = retriever.get_context_for_query(query, top_k=2)
        print(context[:200] + "..." if len(context) > 200 else context)


if __name__ == "__main__":
    # 初始化并测试检索系统
    init_retrieval_system()
    test_retrieval_system()
