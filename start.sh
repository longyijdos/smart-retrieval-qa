#!/bin/bash

# 大语言模型检索增强问答系统启动脚本

echo "==================================================="
echo "   大语言模型检索增强问答系统"
echo "==================================================="
echo

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "错误: 未找到Python，请先安装Python"
    exit 1
fi

# 检查依赖
echo "检查依赖包..."
python -c "import openai, jieba" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "正在安装依赖包..."
    pip install -r requirements.txt
fi

echo "依赖检查完成！"
echo

# 显示可用模型
echo "可用的模型："
echo "1. GPT-4o (默认)"
echo "2. Gemini-1.5-Flash"
echo "3. Claude-3.5-Sonnet"
echo

# 获取用户选择
read -p "请选择模型 (1-3, 默认为1): " choice

case $choice in
    1|"") model="GPT-4o" ;;
    2) model="Gemini-1.5-Flash" ;;
    3) model="Claude-3.5-Sonnet" ;;
    *) 
        echo "无效选择，使用默认模型 GPT-4o"
        model="GPT-4o"
        ;;
esac

echo "启动模型: $model"
echo "==================================================="

# 启动系统
python main.py --model "$model"
