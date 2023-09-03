from fastapi import APIRouter, Depends

from models.events import UserOnRegistration
from models.queue import Message
from services.event import EventService, get_event_service
from services.publisher import RabbitMQPublisher, get_publisher

router = APIRouter()


@router.post("/send")
async def send_message(
    message: Message,
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    # Проверить статус суперпользователя у пользователя

    await publisher.publish_message(message.json())


@router.post("/events/on_registration")
async def on_registration(
    context: UserOnRegistration,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    # Проверить статус суперпользователя у пользователя
    message = event_service.on_registration(context)

    await publisher.publish_message(message.json())
