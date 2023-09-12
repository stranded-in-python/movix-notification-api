from fastapi import APIRouter, Depends

from models.notifications import Notification
from services.publisher import RabbitMQPublisher, get_publisher

router = APIRouter()

@router.post("/send")
async def send_message(
    message: Notification,
    publisher: RabbitMQPublisher = Depends(get_publisher)
) -> None:
    # Проверить статус суперпользователя у пользователя

    await publisher.publish_message(message.json())
