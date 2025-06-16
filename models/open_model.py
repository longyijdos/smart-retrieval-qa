from openai import OpenAI
import openai
import time

class OpenAIClient:
    def __init__(self, base_url, api_key, prompt=None, model="gpt-4o", temperature=0.7):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.prompt = prompt
        self.model = model
        self.temperature = temperature
        self.contents = []
        self.clear_contents()

    def clear_contents(self):
        if self.prompt:
            self.contents = [{"role": "system", "content": self.prompt},
                             {"role": "user", "content": []}]
        else:
            self.contents = [{"role": "user", "content": []}]
    
    def add_message(self, message):
        content = {"type": "text", "text": message}
        self.contents[-1]["content"].append(content)

    def change_prompt(self, new_prompt):
        self.prompt = new_prompt
        self.clear_contents()

    def get_response(self):
        max_attempts = 20  # 最大重试次数
        attempt = 0
        
        while attempt < max_attempts:
            try:
                # 尝试发送请求
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.contents,
                    temperature=self.temperature,
                )
                return completion.choices[0].message.content
            except openai.RateLimitError as e:
                # 捕获限流错误并等待 30 秒后重试
                print(f"Rate limit错误: {e}. 30秒后重试...")
                time.sleep(30)
            except Exception as e:
                # 捕获其他错误并等待后重试
                print(f"发生意外错误: {e}")
                time.sleep(30)
            
            attempt += 1
        return "达到最大尝试次数，请求未成功"
    

