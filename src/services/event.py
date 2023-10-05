from functools import lru_cache

import models.events as events
from core.config import user_properties
from models.queue import EmailTitle, Message, MessageType


class EventService:
    def _create_message(
        self, context: dict, template_id: str, type: MessageType, recipients: list
    ) -> Message:
        return Message(
            context=context, template_id=template_id, type=type, recipients=recipients
        )

    def on_registration(self, user: events.UserOnRegistration):
        event_obj = events.RegistrationEvent()
        context = {
            "verefy_url": user_properties.url_verify,
            "verification_token": user.verification_token,
        }
        email = EmailTitle(
            to_=[user.email], from_=event_obj.send_from, subject=event_obj.subject
        )
        message = self._create_message(
            context, event_obj.template_id, MessageType.email, recipients=email
        )
        return message

    def on_refund(self, user: events.UserOnRefund):
        event_obj = events.RefundEvent()
        context = {"username": user.username, "amount": user.amount}
        email = EmailTitle(
            to_=[user.email], from_=event_obj.send_from, subject=event_obj.subject
        )
        message = self._create_message(
            context, event_obj.template_id, MessageType.email, recipients=email
        )
        return message

    def on_subscription(self, user: events.UserOnSubscription):
        event_obj = events.SubscriptionEvent()
        print(user, '!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        context = {"username": user.username, "sub_name": user.subscription_name}
        email = EmailTitle(
            to_=[user.email], from_=event_obj.send_from, subject=event_obj.subject
        )
        message = self._create_message(
            context, event_obj.template_id, MessageType.email, recipients=email
        )
        return message

    def on_payment_error(self, user: events.UserOnPaymentError):
        event_obj = events.PaymentErrorEvent()
        context = {"username": user.username, "amount": user.amount}
        email = EmailTitle(
            to_=[user.email], from_=event_obj.send_from, subject=event_obj.subject
        )
        message = self._create_message(
            context, event_obj.template_id, MessageType.email, recipients=email
        )
        return message


@lru_cache
def get_event_service():
    return EventService()
