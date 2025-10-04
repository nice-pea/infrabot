import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    tg_token = os.getenv("TG_TOKEN")
    chat_id = int(os.getenv("CHAT_ID"))
    topic_id = int(os.getenv("TOPIC_ID"))
    port = int(os.getenv("PORT", 8080))
    gh_hook_secret = os.getenv("GH_HOOK_SECRET")
    gh_token = os.getenv("GH_TOKEN")
