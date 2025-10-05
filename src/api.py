import json
import logging

from fastapi import APIRouter
from fastapi import HTTPException, Request, Header

from src.config import Config
from src.github_api import verify_signature
from src.telegram_bot_api import handle_event_and_send_message
from src.workflow_event import event_from_workflow_run

router = APIRouter()


@router.get("/")
async def root():
    return "hello"


@router.post("/workflows")
async def workflows(
    request: Request,
    x_hub_signature_256: str = Header(..., alias="X-Hub-Signature-256"),
):
    # Получить тело запроса в виде строки
    data_str = (await request.body()).decode("utf-8")

    # Проверка подписи
    if not verify_signature(data_str, Config.gh_hook_secret, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = json.loads(data_str)
        workflow_run = data["workflow_run"]
        # Создать обрабатываемое событие из workflow_run события
        event = event_from_workflow_run(workflow_run)
        # Обработать событие
        if event is not None:
            await handle_event_and_send_message(event)
    except Exception as e:
        logging.debug(e)
        raise HTTPException(status_code=500, detail=str(e))
