import traceback
from typing import Any, Dict, Union, Callable, Awaitable

from aiogram import BaseMiddleware, types

from project.services.user_service import UserService, UserUpsert


# from project import check_user, get_lang, bot


class DefaultMiddleware(BaseMiddleware):
    def __init__(self, locales):
        self.user = None
        self.locales = locales

    async def __call__(self, handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]], event: [types.Message, types.CallbackQuery], data: Dict[str, Any]) -> Any:
        user_service = UserService()

        try:
            upsert_user = UserUpsert(
                user_telegram_id=str(event.from_user.id),
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name or "",
                username=event.from_user.username or "",
                language_code=event.from_user.language_code,
                is_premium=event.from_user.is_premium or False
            )
            print(upsert_user.model_dump())
            await user_service.upsert_user(upsert_user)

        except Exception:
            print(traceback.format_exc())

        finally:
            await user_service.close()

        # get lang impl
        user_lang = "ru"
        lang = self.locales.get(user_lang)

        data["lang"] = lang

        return await handler(event, data)
