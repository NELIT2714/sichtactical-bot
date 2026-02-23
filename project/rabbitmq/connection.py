import aio_pika
import os


async def get_connection():
    return await aio_pika.connect_robust(
        host=os.getenv("RABBITMQ_HOST"),
        port=int(os.getenv("RABBITMQ_PORT")),
        login=os.getenv("RABBITMQ_USERNAME"),
        password=os.getenv("RABBITMQ_PASSWORD"),
        virtualhost=os.getenv("RABBITMQ_VHOST", "/"),
    )