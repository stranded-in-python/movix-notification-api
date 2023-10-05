from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from api.v1.common import ErrorCode
from core.config import user_properties
from models.events import (
    UserOnPaymentError,
    UserOnRefund,
    UserOnRegistration,
    UserOnSubscription,
)
from models.queue import EmailTitle, Message
from models.users import UserChannels
from services.event import EventService, get_event_service
from services.notification import NotificationService, get_notification_service
from services.publisher import RabbitMQPublisher, get_publisher
from services.user import UserService, get_user_service

router = APIRouter()


@router.post("/message", response_model=None)
async def post_message(
    message: Message, publisher: RabbitMQPublisher = Depends(get_publisher)
) -> None:
    await publisher.publish_message(message.json())


@router.post("/events/registration/on", response_model=None)
async def on_registration(
    context: UserOnRegistration,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> None:
    message = event_service.on_registration(context)

    await publisher.publish_message(message.json())


@router.post("/events/refund/on", response_model=None)
async def on_refund(
    context: UserOnRefund,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> Response(status_code=status.HTTP_200_OK):
    message = event_service.on_refund(context)

    await publisher.publish_message(message.json())


@router.post("/events/subscription/on", response_model=None)
async def on_subscription(
    context: UserOnSubscription,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> Response(status_code=status.HTTP_200_OK):
    message = event_service.on_subscription(context)

    await publisher.publish_message(message.json())


@router.post("/events/payment-error/on", response_model=None)
async def on_payment_error(
    context: UserOnPaymentError,
    event_service: EventService = Depends(get_event_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
) -> Response(status_code=status.HTTP_200_OK):
    message = event_service.on_payment_error(context)

    await publisher.publish_message(message.json())


@router.post("/{id_notification}", response_model=None)
async def generate_notifiaction(
    id_notification: UUID,
    user_service: UserService = Depends(get_user_service),
    notification_service: NotificationService = Depends(get_notification_service),
    publisher: RabbitMQPublisher = Depends(get_publisher),
):
    notification = await notification_service.get_notification(id_notification)

    if notification is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail=ErrorCode.NOTIFICATION_NOT_FOUND
        )

    async for users_ids in notification_service.get_notification_users(id_notification):
        users_channels = await user_service.get_users_channels(users_ids)  # type: ignore

        for channel_type in notification.channels:
            users_channels: list[UserChannels] = [
                user_channels
                for user_channels in users_channels
                for channel in user_channels.channels
                if channel.type == channel_type
            ]

            recipients: list[str] = [
                channel.value
                for user_channels in users_channels
                for channel in user_channels.channels
            ]

            _recipients = EmailTitle(
                to_=recipients,  # type: ignore
                from_=user_properties.notifications_email_from,  # type: ignore
                subject=notification.title,
            )
            context = await notification_service.generate_context(
                notification, (user_channels.id for user_channels in users_channels)  # type: ignore
            )
            message = Message(
                context=context,  # type: ignore
                template_id=notification.template_id,
                type=channel_type,  # type: ignore
                recipients=_recipients,
            )

            await publisher.publish_message(message.json())
