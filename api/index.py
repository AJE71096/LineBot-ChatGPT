import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.prompt import Prompt
from openai import OpenAI

# 初始化 LINE Bot API 和 WebhookHandler
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default="true").lower() == "true"

app = Flask(__name__)
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# 定義 Prompt 類別
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

# 定義 ChatGPT 類別
class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default="gpt-4")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default=0))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default=500))

    def get_response(self):
        response = client.chat.completions.create(
            model=self.model,
            messages=self.prompt.generate_prompt(),
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

    def add_msg(self, role, text):
        self.prompt.add_msg(role, text)

chatgpt = ChatGPT()

# 定義 Flask 路由
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return
    
    if event.message.text == "啟動":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="我是時下流行的AI智能，目前可以為您服務囉，歡迎來跟我互動~"))
        return

    if event.message.text == "安靜":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="感謝您的使用，若需要我的服務，請跟我說 「啟動」 謝謝~"))
        return
    
    if working_status:
        chatgpt.add_msg("user", event.message.text)
        reply_msg = chatgpt.get_response()
        chatgpt.add_msg("assistant", reply_msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

if __name__ == "__main__":
    app.run()
