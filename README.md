# 大语言模型检索增强问答系统

基于大语言模型的检索增强生成（RAG）系统，能够从参考文档中检索相关片段，并结合用户问题生成更准确的回答。

## 功能特性

- 🔍 **智能检索**: 从参考文档中自动检索相关内容片段
- 🤖 **多模型支持**: 支持 GPT-4o、Gemini-1.5-Flash、Claude-3.5-Sonnet
- 📚 **文档增强**: 自动将检索到的文档内容与用户问题结合
- 💬 **对话交互**: 支持连续对话和上下文记忆
- 🚀 **简单易用**: 命令行界面，操作简便

## 项目结构

```
LLM/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── requirements.txt     # 依赖包列表
├── test_retrieval.py    # 检索功能测试脚本
├── models/              # 模型相关模块
│   ├── __init__.py
│   ├── mapping.py       # 模型映射配置
│   └── open_model.py    # OpenAI客户端实现
├── ref/                 # 检索相关模块
│   ├── init.py          # 检索系统初始化
│   ├── retrive.py       # 文本检索核心逻辑
│   └── ref.txt          # 参考文档
└── utils/               # 工具模块
    ├── __init__.py
    └── attr_dict.py     # 属性字典工具
```

## 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `openai>=1.0.0`: OpenAI API客户端
- `jieba>=0.42.1`: 中文分词库
- `prompt_toolkit==3.0.51`: 兼容中文输入

## 使用方法

### 基本使用

```bash
python main.py --model GPT-4o
```

### 参数说明

- `--model`: 指定使用的模型（GPT-4o, Gemini-1.5-Flash, Claude-3.5-Sonnet）
- `--prompt`: 自定义系统提示词
- `--temperature`: 控制回答的随机性（0.0-1.0）

### 交互命令

- 输入问题：直接输入你的问题
- `clear`：清除对话历史
- `exit` 或 `quit`：退出程序

## 工作原理

1. **文档预处理**: 系统启动时自动加载 `ref/ref.txt` 文档并分割成小块
2. **查询检索**: 用户输入问题后，系统使用TF-IDF相似度计算检索相关文档片段
3. **内容增强**: 将检索到的相关片段与用户问题拼接，形成增强的prompt
4. **模型生成**: 将增强后的prompt发送给大语言模型生成回答

## 检索算法

使用基于词频-逆文档频率(TF-IDF)的文本相似度计算：

1. **分词处理**: 使用jieba进行中文分词
2. **相似度计算**: 计算查询与文档片段的词汇重叠度
3. **排序筛选**: 按相似度排序，返回最相关的前K个片段

## 测试功能

测试检索功能：
```bash
python test_retrieval.py
```

测试检索系统初始化：
```bash
python ref/init.py
```

## 配置说明

在 `config.py` 中配置API密钥和基础URL：

```python
__C.OPENAI.URL = "https://your-api-endpoint.com/v1"
__C.OPENAI.KEY = {
    "GPT-4o": "your-gpt4o-api-key",
    "Gemini-1.5-Flash": "your-gemini-api-key", 
    "Claude-3.5-Sonnet": "your-claude-api-key"
}
```

## 示例对话

```
用户: 什么是大语言模型？

AI: 根据文档内容，大语言模型（Large Language Model，简称LLM）是一种基于深度学习的人工智能技术，也是自然语言处理的核心研究内容之一。其核心特点包括：

1. **技术原理**: 使用大规模数据集对模型进行训练，使其能够生成自然语言文本或理解语言文本的含义
2. **架构特点**: 通过层叠的神经网络结构，学习并模拟人类语言的复杂规律
3. **能力水平**: 能够达到接近人类水平的文本生成能力

大语言模型采用与小模型类似的Transformer架构和预训练目标，主要区别在于大幅增加了模型大小、训练数据和计算资源。
```

## 注意事项

1. 确保API密钥配置正确
2. 检查网络连接是否正常
3. 第一次运行会自动下载jieba分词模型
4. 参考文档可以根据需要替换或更新

## 故障排除

**Q: 提示"无法解析导入jieba"**
A: 运行 `pip install jieba` 安装分词库

**Q: 模型响应出错**
A: 检查API密钥是否正确，网络连接是否正常

**Q: 检索结果不准确**
A: 可以调整检索参数或更新参考文档内容

## 扩展功能

- 支持更多文档格式（PDF, Word等）
- 实现更高级的检索算法（向量检索、语义匹配）
- 添加Web界面
- 支持多文档检索
