import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default="50"))
LANGUAGE_TABLE = {
    "zh": "哈囉！",
    "en": "Hello!"
}

AI_GUIDELINES = '你是一個AI資訊助手，會簡單明瞭的提供用戶想要的資訊'

class Prompt:
    def __init__(self):
        self.msg_list = []
        self.msg_list.append({
            "role": "system", 
            "content": f"{LANGUAGE_TABLE[chat_language]}, {AI_GUIDELINES}"
        })
    
    def add_msg(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.msg_list.pop(0)
        self.msg_list.append({"role": "user", "content": new_msg})

    def generate_prompt(self):
        return self.msg_list
