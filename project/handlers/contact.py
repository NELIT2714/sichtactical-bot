import traceback

from aiogram import F
from aiogram import Router
from aiogram.types import Message

from project.services.user_service import UserService, UserUpsert

router = Router()


@router.message(F.contact)
async def got_contact(message: Message):
    user_service = UserService()

    user_telegram_id = str(message.contact.user_id)
    phone_number = message.contact.phone_number
    phone_number = phone_number if phone_number.startswith("+") else f"+{phone_number}"

    try:
        upsert_phone_number = UserUpsert(
            user_telegram_id=user_telegram_id,
            phone_number=phone_number
        )
        print(upsert_phone_number.model_dump())
        await user_service.upsert_user(upsert_phone_number)
    except:
        print(traceback.format_exc())

    finally:
        await user_service.close()

    await message.delete()
