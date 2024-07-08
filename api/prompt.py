import os

# 獲取初始化語言環境變量，默認為中文
chat_language = os.getenv("INIT_LANGUAGE", default="zh")

# 設置消息列表的最大長度，默認為20
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))

# 語言表，根據不同語言顯示對應的問候語
LANGUAGE_TABLE = {
    "zh": "嗨！",
    "en": "Hi!"
}

class Prompt:
    def __init__(self):
        # 初始化消息列表並添加初始消息
        self.msg_list = [f"AI:{LANGUAGE_TABLE[chat_language]}"]
    
    def add_msg(self, new_msg):
        # 如果消息列表超過限制，移除最早的消息
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        # 添加新消息到列表
        self.msg_list.append(new_msg)

    def remove_msg(self):
        # 移除最早的消息
        self.msg_list.pop(0)

    def generate_prompt(self):
        # 生成最終的提示信息
        return '\n'.join(self.msg_list)
