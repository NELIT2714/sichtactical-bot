import traceback

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.enums import ParseMode

from project.services.user_service import UserService, UserUpsert

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, lang: dict):
    return await message.bot.send_message(
        chat_id=message.from_user.id,
        text=lang["messages"]["start"],
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=lang["buttons"]["open_webapp"],
                    web_app=WebAppInfo(url="https://sichtactical.vercel.app/")
                )
            ]
        ]),
        parse_mode=ParseMode.MARKDOWN
    )
