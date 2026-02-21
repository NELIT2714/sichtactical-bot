import asyncio
import logging

from project.config.main import setup


async def run_bot():
    logging.basicConfig(level=logging.INFO)
    bot, dp = setup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
