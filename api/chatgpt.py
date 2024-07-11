import os
from api.prompt import Prompt
from openai import OpenAI
client = OpenAI()

client.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()  # 初始化 Prompt 物件
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")  # 設定模型名稱
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0.5))  # 設定"創造力"程度
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=150))  # 設定最大tokens數量

    def get_response(self):
        # 使用OpenAI的chatGPT模型獲取回應訊息
        response = client.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
        )
        return response.choices[0].message.content

    def add_msg(self, text):
        # 將訊息新增到Prompt物件中
        self.prompt.add_msg(text)
