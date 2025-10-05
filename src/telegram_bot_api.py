import json
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, Update
from telegram.ext import Application, CallbackQueryHandler, CallbackContext

from src.config import Config
from src.github_api import deploy_workflow_dispatch
from src.workflow_event import WorkflowFailed, DeliverySuccess, WorkflowSuccess

bot = Bot(token=Config.tg_token)


async def on_unknown_callback(update: Update, context: CallbackContext):
    logging.info(update)


async def on_deploy_callback(update: Update, context: CallbackContext):
    ref = update.callback_query.data.split("/")[-1]
    deploy_workflow_dispatch(ref)


# Запустить бота
app = Application.builder().token(Config.tg_token).build()
app.add_handlers(
    [
        CallbackQueryHandler(on_deploy_callback, pattern="^/deploy/\w+$"),
        CallbackQueryHandler(on_unknown_callback),
    ]
)


# Обработать событие и отправить сообщение
async def handle_event_and_send_message(event: object | WorkflowFailed | WorkflowSuccess | DeliverySuccess):
    if isinstance(event, WorkflowFailed):
        workflow_run = event.workflow_run
    elif isinstance(event, WorkflowSuccess):
        workflow_run = event.workflow_run
    elif isinstance(event, DeliverySuccess):
        workflow_run = event.workflow_run
        markup = markup_with_deploy_btn(workflow_run)
    else:
        logging.info("Unknown event type")
        return

    await bot.send_message(
        chat_id=Config.chat_id,
        message_thread_id=Config.topic_id,
        text=telegram_text_from_workflow_run(workflow_run),
        reply_markup=,
    )


def markup_with_deploy_btn(workflow_run) -> InlineKeyboardMarkup | None:
    # if (
    #     workflow_run["status"] != "completed"
    #     or workflow_run["conclusion"] != "success"
    #     or workflow_run["name"] != "Delivery"
    # ):
    #     return None

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


def delivery_text(workflow_run) -> str:
    pass


def deploy_text(workflow_run: dict) -> str:
    pass
