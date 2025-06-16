#!/usr/bin/env python3
"""
简单的测试脚本，用于验证检索增强的问答系统
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ref.init import init_retrieval_system
from ref.retrive import get_retriever

def test_retrieval_only():
    """仅测试检索功能"""
    print("=" * 60)
    print("测试检索功能")
    print("=" * 60)
    
    # 初始化检索系统
    retriever = init_retrieval_system()
    if retriever is None:
        print("检索系统初始化失败")
        return
    
    # 测试查询
    test_queries = [
        "什么是大语言模型？",
        "GPT-4有什么特点？",
        "大语言模型在教育领域的应用",
        "强化学习的作用",
        "大语言模型的局限性"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. 查询: {query}")
        print("-" * 40)
        
        # 获取检索结果
        results = retriever.retrieve(query, top_k=3)
        
        if results:
            for j, result in enumerate(results, 1):
                print(f"相关片段 {j} (相似度: {result['similarity']:.4f}):")
                content = result['content']
                # 限制显示长度
                if len(content) > 200:
                    content = content[:200] + "..."
                print(content)
                print()
        else:
            print("未找到相关内容")
        
        print("-" * 60)

def main():
    print("大语言模型检索增强问答系统 - 测试脚本")
    test_retrieval_only()

if __name__ == "__main__":
    main()
