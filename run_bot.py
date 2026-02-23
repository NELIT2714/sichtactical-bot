import asyncio
import logging

from project.config.main import setup
from project.rabbitmq.consumer import start_consumer


async def run():
    logging.basicConfig(level=logging.INFO)
    bot, dp, lang = setup()

    await asyncio.gather(
        dp.start_polling(bot),
        start_consumer(bot, lang)
    )

if __name__ == "__main__":
    asyncio.run(run())
