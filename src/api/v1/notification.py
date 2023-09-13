from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.common import ErrorCode
from core.config import user_propertis
from models.events import UserOnRegistration
from models.queue import EmailTitle, Message
from services.event import EventService, get_event_service
from services.notification import NotificationService, get_notification_service
from services.publisher import RabbitMQPublisher, get_publisher
from services.user import UserService, get_user_service

router = APIRouter()


@router.post("/message", response_model=None)
async def post_message(
    message: Message, publisher: RabbitMQPublisher = Depends(get_publisher)
) -> None:
    # Проверить статус суперпользователя у пользователя

    await publisher.publish_message(message.json())


@router.post("/events/registration/on", response_model=None)
async def on_registration(
    context: UserOnRegistration,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    message = event_service.on_registration(context)

    await publisher.publish_message(message.json())


# Сформировать задание рассылки уведомления
@router.post("/{id_notification}", response_model=None)
async def generate_notifiaction(
    id_notification: UUID,
    user_service: UserService = Depends(get_user_service),
    notification_service: NotificationService = Depends(get_notification_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
):
    # Получить данные уведомления
    notification = await notification_service.get_notification(id_notification)

    if notification is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=ErrorCode.NOTIFICATION_NOT_FOUND
        )

    async for users_ids in notification_service.get_notification_users(id_notification):
        users_channels = await user_service.get_users_channels(users_ids)

        for channel_type in notification.channels:
            recipients = [
                channel
                for user_channels in users_channels
                for channel in user_channels.channels
                if channel.type == channel_type
            ]
            _recipients = EmailTitle(
                to_=[channel.value for channel in recipients],
                from_=user_propertis.notifications_email_from,
                subject=notification.title,
            )
            print(recipients)
            # сформировать Message
            message = Message(
                context=notification.context,
                template_id=notification.template_id,
                type=channel_type,
                recipients=_recipients,
            )

            await publisher.publish_message(message.json())
