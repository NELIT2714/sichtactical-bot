import asyncio
import logging
from aiogram import Bot

from project.rabbitmq.handlers import new_event
from project.rabbitmq.connection import get_connection

logger = logging.getLogger(__name__)


async def start_consumer(bot: Bot, lang: dict):
    while True:
        try:
            connection = await get_connection()
            logger.info("RabbitMQ connected")

            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)

                await asyncio.gather(
                    new_event.start(bot, channel, lang),
                    # promo.start(bot, channel),  # добавляй новые хендлеры сюда
                    # system.start(bot, channel),
                )

        except Exception as e:
            logger.error(f"RabbitMQ error: {e}. Reconnecting in 5s...")
            await asyncio.sleep(5)
