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
    gh_repo = os.getenv("GH_REPO")
    gh_owner = os.getenv("GH_OWNER")
    gh_workflow_deploy = os.getenv("GH_WORKFLOW_DEPLOY")
    gh_workflow_delivery = os.getenv("GH_WORKFLOW_DELIVERY")
