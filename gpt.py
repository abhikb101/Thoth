from settings import OPENAI_API_KEY, OPENAI_ENGINE
from revChatGPT.V3 import Chatbot
import time

if OPENAI_ENGINE:
    ChatGPTConfig["engine"] = os.getenv("OPENAI_ENGINE")
    
ChatGPTConfig = {
    "api_key": OPENAI_API_KEY,
}

chatbot = Chatbot(**ChatGPTConfig)

def chatgpt_refresh():
    while True:
        time.sleep(60)