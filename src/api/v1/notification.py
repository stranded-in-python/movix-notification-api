from uuid import UUID

from fastapi import APIRouter, Depends

from models.events import UserOnRegistration
from models.queue import Message
from services.event import EventService, get_event_service
from services.notification import NotificationService, get_notification_service
from services.publisher import RabbitMQPublisher, get_publisher
from services.user import UserService, get_user_service

router = APIRouter()


@router.post("/message")
async def post_message(
    message: Message,
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    # Проверить статус суперпользователя у пользователя

    await publisher.publish_message(message.json())


@router.post("/events/registration/on")
async def on_registration(
    context: UserOnRegistration,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    message = event_service.on_registration(context)

    await publisher.publish_message(message.json())


# Сформировать задание рассылки уведомления
@router.post("/{id_notification}")
async def generate_notifiaction(
    id_notification: UUID,
    user_service: UserService = Depends(get_user_service),
    notification_service: NotificationService = Depends(get_notification_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    # Получить данные уведомления
    # notification = notification_service.get_notification(id_notification)

    # Получить пачку пользователей
    user_list_is_empty = False

    while not user_list_is_empty:
        offset = 0
        user_ids, offset = notification_service.get_users(id_notification, offset)

        # Получить настройи уведомлений
        # user_settings = user_service.get_users_settings(user_ids)

        # Для каждого канала
        # for channel in
        #     # сформировать Message
        #     message = Message(
        #         context=notification.context,
        #         template_id=notification.template_id,
        #         type=notification., # Откуда берётся тип уведомления
        # )
        # Отправить в очередь
