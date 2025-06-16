import argparse
import os
import sys
from prompt_toolkit import prompt
from models import get_model

# 添加ref模块到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'ref'))
from ref.init import init_retrieval_system
from ref.retrive import get_retriever

def main():
    # 打印配置信息
    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}")
    print(f"Temperature: {args.temperature}")
    print("=" * 50)
    
    # 初始化检索系统
    print("正在初始化检索系统...")
    retriever = init_retrieval_system()
    if retriever is None:
        print("警告: 检索系统初始化失败，将使用原始prompt")
    
    # 获取模型
    model = get_model(args)
    print("模型初始化完成")
    print("=" * 50)
    print("开始对话 (输入 'exit' 或 'quit' 退出，输入 'clear' 清除对话历史)")
    print("=" * 50)

    while True:
        user_input = prompt("\n用户: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("退出程序。")
            break
            
        if user_input.lower() == "clear":
            model.clear_contents()
            print("已清除对话内容。")
            continue
        
        # 使用检索系统获取相关文档片段
        if retriever is not None:
            try:
                # 获取相关文档内容
                context = retriever.get_context_for_query(user_input, top_k=3)
                
                # 构建增强的prompt
                enhanced_message = f"""请严格按照以下优先级回答用户问题：

1. **优先级1**: 如果以下文档片段中包含相关信息，请主要基于文档内容进行回答
2. **优先级2**: 如果文档片段信息不足或不相关，再结合你的知识库补充回答
3. **重要**: 请明确标注哪些内容来自文档，哪些来自你的知识库

--- 文档片段 ---
{context}
--- 文档片段结束 ---

用户问题: {user_input}

回答格式建议：
- 如果文档有相关信息：先说"根据提供的文档..."，然后基于文档回答
- 如果需要补充信息：明确说明"文档中未涉及的补充信息..."
- 如果文档完全不相关：说明"文档中没有找到相关信息，基于通用知识..."
"""
                
                print("正在检索相关文档并生成回答...")
                
            except Exception as e:
                print(f"检索过程中出错: {e}")
                enhanced_message = user_input
        else:
            enhanced_message = user_input
        
        # 发送消息给模型
        model.add_message(enhanced_message)
        
        try:
            response = model.get_response()
            print(f"\nAI: {response}")
        except Exception as e:
            print(f"模型响应出错: {e}")
            print("请稍后重试。")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argument parsing.")
    parser.add_argument("--model", type=str, default="GPT-4o", help="Model to use for the request.")
    parser.add_argument("--prompt", type=str, default="请你根据以下文档内容，回答用户提出的问题。", help="Prompt to use for the model.")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature for the model response.")

    args = parser.parse_args()

    main()