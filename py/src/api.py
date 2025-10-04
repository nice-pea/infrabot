import hashlib
import hmac
import json
import logging

from fastapi import APIRouter
from fastapi import HTTPException, Request, Header
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton

from src.config import Config

router = APIRouter()

bot = Bot(token=Config.tg_token)


@router.get("/")
async def root():
    return "hello"


@router.post("/workflows")
async def workflows(
    request: Request,
    x_hub_signature_256: str = Header(..., alias="X-Hub-Signature-256"),
):
    data_bytes = await request.body()
    data_str = data_bytes.decode("utf-8")

    # Проверка подписи
    if not verify_signature(data_str, Config.gh_hook_secret, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = json.loads(data_str)
        workflow_run = data["workflow_run"]
        if (
            workflow_run["status"] != "completed"
            and workflow_run["conclusion"] != "success"
            and workflow_run["conclusion"] != "failed"
        ):
            return None

        await bot.send_message(
            chat_id=Config.chat_id,
            message_thread_id=Config.topic_id,
            text=telegram_text_from_workflow_run(workflow_run),
            reply_markup=telegram_markup_from_workflow_run(workflow_run),
        )
        return {"status": "Message sent successfully"}
    except Exception as e:
        logging.debug(e)
        raise HTTPException(status_code=500, detail=str(e))


def telegram_markup_from_workflow_run(workflow_run) -> InlineKeyboardMarkup | None:
    if (
        workflow_run["status"] != "completed"
        or workflow_run["conclusion"] != "success"
        or workflow_run["name"] != "Delivery"
    ):
        return None

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Deploy",
                    callback_data={
                        "action": "deploy",
                        "id": workflow_run["id"],
                    },
                )
            ]
        ]
    )


def telegram_text_from_workflow_run(workflow_run: dict) -> str:
    if workflow_run["conclusion"] != "success":
        return f"неудача :(\nworkflow: :{workflow_run["name"]}\nurl: {workflow_run["html_url"]}"

    if workflow_run["name"] == "Deploy":
        return deploy_text(workflow_run)
    elif workflow_run["name"] == "Delivery":
        return delivery_text(workflow_run)

    return json.dumps(
        {
            "id": workflow_run["id"],
            "name": workflow_run["name"],
            "head_branch": workflow_run["head_branch"],
            "status": workflow_run["status"],
            "conclusion": workflow_run["conclusion"],
            "actor": workflow_run["triggering_actor"]["login"],
            "event": workflow_run["event"],
        },
        indent=4,
    )


def delivery_text(workflow_run):
    pass


def deploy_text(workflow_run: dict) -> str:
    pass


def verify_signature(payload: str, secret: str, signature: str) -> bool:
    """Проверяет подпись от GitHub."""
    hmac_obj = hmac.new(secret.encode(), payload.encode(), hashlib.sha256)
    digest = hmac_obj.hexdigest()
    expected_signature = f"sha256={digest}"
    return hmac.compare_digest(expected_signature, signature)

def deploy_workfloy_dispatch(ref: str):
    # curl -L \
    # -X POST \
    #    -H "Accept: application/vnd.github+json" \
    #       -H "Authorization: Bearer <YOUR-TOKEN>" \
    #          -H "X-GitHub-Api-Version: 2022-11-28" \
    #         https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/dispatches \
    #                 -d '{"ref":"topic-branch","inputs":{"name":"Mona the Octocat","home":"San Francisco, CA"}}'
    pass