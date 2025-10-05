import json
import logging
from dataclasses import asdict

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Bot,
    Update,
)
from telegram.ext import Application, CallbackQueryHandler, CallbackContext

from src.config import Config
from src.github_api import deploy_workflow_dispatch
from src.workflow_event import (
    DeliveryJobSuccess,
    Event,
    WorkflowFailed,
    WorkflowSuccess,
)

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
        CallbackQueryHandler(on_deploy_callback, pattern="^/deploy/\\w+$"),
        CallbackQueryHandler(on_unknown_callback),
    ]
)


# Обработать событие и отправить сообщение
async def handle_event_and_send_message(event: Event):
    await bot.send_message(
        chat_id=Config.chat_id,
        message_thread_id=Config.topic_id,
        text=telegram_text_from_event(event),
        reply_markup=markup_with_deploy_btn(event),
        disable_web_page_preview=True,
        # link_preview_options=LinkPreviewOptions.is_disabled,
    )


def markup_with_deploy_btn(event: Event) -> InlineKeyboardMarkup | None:
    if not isinstance(event, DeliveryJobSuccess):
        return None

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Deploy",
                    callback_data={
                        "action": "deploy",
                        "tag": event.tag,
                    },
                )
            ]
        ]
    )


def telegram_text_from_event(event: Event) -> str:
    if isinstance(event, WorkflowFailed) or isinstance(event, WorkflowSuccess):
        return "\n".join(f"{k} = {v}" for k, v in asdict(event.workflow).items())
    elif isinstance(event, DeliveryJobSuccess):
        return (
            "\n".join(f"{k} = {v}" for k, v in asdict(event.job).items())
            + f"\n{event.tag}"
        )

    return json.dumps(asdict(event), indent=1, ensure_ascii=False)


def delivery_text(workflow_run) -> str:
    pass


def deploy_text(workflow_run: dict) -> str:
    pass
