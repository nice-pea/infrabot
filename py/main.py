import json
import logging
import os
import hmac
import hashlib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Header
from telegram import Bot
import uvicorn

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# Параметры из .env
tg_token = os.getenv('TG_TOKEN')
chat_id = int(os.getenv('CHAT_ID'))
topic_id = int(os.getenv('TOPIC_ID'))
port = int(os.getenv('PORT', 8080))
gh_secret = os.getenv('GH_SECRET')

bot = Bot(token=tg_token)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/workflows")
async def workflows(
        request: Request,
        x_hub_signature_256: str = Header(..., alias="X-Hub-Signature-256")
):
    data_bytes = await request.body()
    data_str = data_bytes.decode("utf-8")

    # Проверка подписи
    if not verify_signature(data_str, gh_secret, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = json.loads(data_str)
        workflowRun = data["workflow_run"]
        message = {
            "id": workflowRun["id"],
            "name": workflowRun["name"],
            "head_branch": workflowRun["head_branch"],
            "status": workflowRun["status"],
            "conclusion": workflowRun["conclusion"],
            "actor": workflowRun["triggering_actor"]["login"],
            "event": workflowRun["event"],
        }
        await bot.send_message(chat_id=chat_id, message_thread_id=topic_id, text=json.dumps(message, indent=4))
        return {"status": "Message sent successfully"}
    except Exception as e:
        logging.debug(e)
        raise HTTPException(status_code=500, detail=str(e))


def verify_signature(payload: str, secret: str, signature: str) -> bool:
    """Проверяет подпись от GitHub."""
    hmac_obj = hmac.new(secret.encode(), payload.encode(), hashlib.sha256)
    digest = hmac_obj.hexdigest()
    expected_signature = f"sha256={digest}"
    return hmac.compare_digest(expected_signature, signature)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=port)