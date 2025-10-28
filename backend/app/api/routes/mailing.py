from fastapi import APIRouter, Depends, HTTPException
import aio_pika
import json
from typing import List

from core.config import RABBITMQ_URL
from app.api.depends import get_current_user
from bot.models import User

router = APIRouter(prefix="/mailing", tags=["mailing"])


@router.post("/bulk")
async def bulk_mailing(payload: dict, user: User = Depends(get_current_user)):
    title = payload.get("title")
    text = payload.get("text")

    if not title or not text:
        raise HTTPException(status_code=400, detail="Missing title or text")
    if not user.is_staff:
        raise HTTPException(status_code=403, detail="Forbidden")

    users_list: List[int] = [user.user_id for user in await User.find_all().to_list()]

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.declare_queue("mailing", durable=True)

        for user_id in users_list:
            body = json.dumps(
                {"user_id": user_id, "message_text": f"{title}\n\n{text}"}
            ).encode()
            await channel.default_exchange.publish(
                aio_pika.Message(body=body),
                routing_key="mailing",
            )

    return {"status": "ok"}
