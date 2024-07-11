import os

# 初始化語言
chat_language = os.getenv("INIT_LANGUAGE", default="zh")

# 設置訊息列表的最大限制
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=100))

# 語言表
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}

# AI指導方針
AI_GUIDELINES = '你是一個AI資訊助手，會簡單明瞭的提供用戶想要的資訊，跟回答他們的問題'

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.topic = None  # 追蹤對話主题
        self.msg_list.append(
            {
                "role": "system",
                "content": f"{LANGUAGE_TABLE.get(chat_language, '哈囉！')}, {AI_GUIDELINES}"
            }
        )

    def add_msg(self, new_msg, role="user"):
        # 如果訊息列表達到最大限制，刪除最早的一條訊息
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.msg_list.pop(0)
        # 添加新的訊息
        self.msg_list.append({"role": role, "content": new_msg})

    def generate_prompt(self):
        # 返回訊息列表
        return self.msg_list

    def ask(self, question):
        # 添加用戶問題
        self.add_msg(question, role="user")
        # 模擬AI回覆
        answer = self.answer_question(question)
        # 添加AI回覆
        self.add_msg(answer, role="assistant")
        # 返回整個對話列表
        return self.generate_prompt()

    def answer_question(self, question):
        # 簡單的回覆邏輯，可以替換為更複雜的回覆生成
        if not self.topic:
            self.topic = question  # 設定對話主题
        return f"這是關於 {self.topic} 的回答: {question} 的回覆內容"
