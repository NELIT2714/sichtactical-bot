import dotenv
import os

from aiogram import Bot

dotenv.load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))

