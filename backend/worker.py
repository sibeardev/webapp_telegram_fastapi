import asyncio
import logging
import json
import aio_pika

from core.config import RABBITMQ_URL
from bot.sender import send_message

logger = logging.getLogger(__name__)


async def connect(url):
    for _ in range(10):
        try:
            return await aio_pika.connect_robust(url)
        except aio_pika.exceptions.AMQPConnectionError:
            await asyncio.sleep(10)
    raise RuntimeError("Cannot connect to RabbitMQ")


async def main():
    connection = await connect(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("mailing", durable=True)

    async with queue.iterator() as q:
        async for message in q:
            async with message.process():
                body = message.body.decode()
                data = json.loads(body)
                user_id = data.get("user_id")
                message_text = data.get("message_text")
                await send_message(user_id, message_text)


if __name__ == "__main__":
    asyncio.run(main())
