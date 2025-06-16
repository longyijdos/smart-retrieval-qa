import re
from collections import Counter
import os

# 尝试导入jieba，如果没有则使用简单的分词方法
try:
    import jieba
    # 禁用jieba的日志输出
    jieba.setLogLevel(20)  # 设置为INFO级别，避免调试信息
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False
    print("警告: 未安装jieba库，将使用简单分词。建议运行: pip install jieba")


class TextRetriever:
    def __init__(self, file_path=None):
        self.file_path = file_path or os.path.join(os.path.dirname(__file__), 'ref.txt')
        self.chunks = []
        self.load_text()
    
    def load_text(self):
        """加载并分割文本文件"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按段落分割文本，每个段落作为一个检索单元
            paragraphs = content.split('\n')
            self.chunks = []
            
            current_chunk = ""
            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                if not paragraph:
                    if current_chunk:
                        self.chunks.append(current_chunk.strip())
                        current_chunk = ""
                    continue
                
                # 如果当前块太长，先保存
                if len(current_chunk) > 500 and paragraph:
                    self.chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    if current_chunk:
                        current_chunk += "\n" + paragraph
                    else:
                        current_chunk = paragraph
            
            # 添加最后一个块
            if current_chunk:
                self.chunks.append(current_chunk.strip())
                
            print(f"成功加载文档，共分割为 {len(self.chunks)} 个片段")
            
        except FileNotFoundError:
            print(f"文件 {self.file_path} 未找到")
            self.chunks = []
        except Exception as e:
            print(f"加载文件时出错: {e}")
            self.chunks = []
    
    def preprocess_text(self, text):
        """预处理文本：分词和去除标点"""
        # 去除标点符号
        text = re.sub(r'[^\w\s]', ' ', text)
        
        if HAS_JIEBA:
            # 使用jieba分词
            words = list(jieba.cut(text.lower()))
        else:
            # 简单的空格分词
            words = text.lower().split()
        
        # 过滤掉长度小于2的词
        words = [word.strip() for word in words if len(word.strip()) >= 2]
        return words
    
    def calculate_similarity(self, query_words, chunk_words):
        """计算查询和文本片段的相似度"""
        if not query_words or not chunk_words:
            return 0.0
        
        # 计算词频
        query_counter = Counter(query_words)
        chunk_counter = Counter(chunk_words)
        
        # 计算交集
        intersection = set(query_counter.keys()) & set(chunk_counter.keys())
        
        if not intersection:
            return 0.0
        
        # 计算TF-IDF风格的相似度
        similarity = 0.0
        for word in intersection:
            # 简单的TF计算
            tf_query = query_counter[word] / len(query_words)
            tf_chunk = chunk_counter[word] / len(chunk_words)
            similarity += tf_query * tf_chunk
        
        return similarity
    
    def retrieve(self, query, top_k=3):
        """检索最相关的文本片段"""
        if not self.chunks:
            return []
        
        query_words = self.preprocess_text(query)
        if not query_words:
            return []
        
        # 计算每个片段的相似度
        similarities = []
        for i, chunk in enumerate(self.chunks):
            chunk_words = self.preprocess_text(chunk)
            similarity = self.calculate_similarity(query_words, chunk_words)
            similarities.append((similarity, i, chunk))
        
        # 按相似度排序
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        # 返回前top_k个最相关的片段
        result = []
        for similarity, idx, chunk in similarities[:top_k]:
            if similarity > 0:  # 只返回有相关性的片段
                result.append({
                    'content': chunk,
                    'similarity': similarity,
                    'index': idx
                })
        
        return result
    
    def get_context_for_query(self, query, top_k=3):
        """为查询获取上下文信息"""
        retrieved_chunks = self.retrieve(query, top_k)
        
        if not retrieved_chunks:
            return "未找到相关信息。"
        
        context = "以下是相关的文档内容：\n\n"
        for i, chunk_info in enumerate(retrieved_chunks, 1):
            context += f"【片段{i}】\n{chunk_info['content']}\n\n"
        
        return context.strip()


# 全局检索器实例
retriever = None

def initialize_retriever(file_path=None):
    """初始化检索器"""
    global retriever
    retriever = TextRetriever(file_path)
    return retriever

def get_retriever():
    """获取检索器实例"""
    global retriever
    if retriever is None:
        retriever = initialize_retriever()
    return retriever
