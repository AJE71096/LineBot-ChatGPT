import os

chat_language = os.getenv("INIT_LANGUAGE", default="zh")
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=20))
LANGUAGE_TABLE = {
    "zh": "嗨！",
    "en": "Hi!"
}

class Prompt:
    def __init__(self):
        self.msg_list = [{"role": "system", "content": LANGUAGE_TABLE[chat_language]}]

    def add_msg(self, role, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.remove_msg()
        self.msg_list.append({"role": role, "content": new_msg})

    def remove_msg(self):
        self.msg_list.pop(0)

    def generate_prompt(self):
        return self.msg_list
