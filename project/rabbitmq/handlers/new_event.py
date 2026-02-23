import json
import logging

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

logger = logging.getLogger(__name__)

QUEUE = "notifications.queue"


def build_message(data: dict) -> str:
    title = data.get("title", "")
    description = data.get("description", "")
    content = data.get("content", "")

    return (
        f"🔔 *{title}*\n\n"
        f"{description}\n\n"
        f"{content}"
    )


def build_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Open App 🚀", url="https://ver")]
    ])


async def start(bot: Bot, channel, locales: dict):
    queue = await channel.declare_queue(QUEUE, durable=True, passive=True)

    async with queue.iterator() as iterator:
        async for message in iterator:
            async with message.process():
                try:
                    payload = json.loads(message.body.decode())
                    print(payload)

                    users = payload.get("users", [])

                    notification = payload.get("notification", {})
                    notification_data = notification.get("notification_data", {})

                    data = notification_data.get("ru") or next(iter(notification_data.values()))
                    text = build_message(data)
                    # keyboard = build_keyboard()

                    for user in users:
                        user_id = user.get("telegram_id")
                        user_lang = locales.get(user.get("language_code", "ru"))

                        try:
                            await bot.send_message(
                                chat_id=int(user_id),
                                text=text,
                                parse_mode="Markdown",
                                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text=user_lang["buttons"]["open_webapp"],
                                            web_app=WebAppInfo(url="https://sichtactical.vercel.app/")
                                        )
                                    ]
                                ]),
                            )
                            logger.info(f"Notification sent to user {user_id}")
                        except Exception as e:
                            logger.error(f"Failed to send to user {user_id}: {e}")
                except Exception as e:
                    logger.error(f"Failed to handle event message: {e}")
