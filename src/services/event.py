from functools import lru_cache

from core.config import events_properties, user_propertis
from core.exceptions import EventNameError
from models.events import UserOnRegistration
from models.queue import EmailTitle, Message, MessageType


class EventService:
    def on_registration(self, user: UserOnRegistration) -> Message:
        event_name = "on_registration"

        template_id = self.get_template_id(event_name)
        context = self.get_template_context(event_name, user)
        recipients = self.get_message_recipients(event_name, user)

        message = self.create_message(
            context, template_id, MessageType.email, recipients
        )

        return message

    def get_template_id(self, event_name):
        match event_name:
            case "on_registration":
                return events_properties.on_registration_template_id

            case _:
                raise EventNameError

    def get_template_context(self, event_name, user):
        match event_name:
            case "on_registration":
                return self._on_registration_context(user)

            case _:
                raise EventNameError

    def _on_registration_context(self, user: UserOnRegistration):
        context = {
            "verefy_url": user_propertis.url_verify,
            "verification_token": user.verification_token,
        }
        return context

    def get_message_recipients(self, event_name, user):
        match event_name:
            case "on_registration":
                return self._on_registration_recipients(user)

            case _:
                raise EventNameError

    def _on_registration_recipients(self, user: UserOnRegistration):
        return EmailTitle(
            to_=[user.email],
            from_=events_properties.on_registration_send_from,
            subject_=events_properties.on_registration_subject,
        )

    def create_message(
        self, context: dict, template_id: str, type: MessageType, recipients: list
    ) -> Message:
        return Message(
            context=context,
            template_id=template_id,
            type=type,
            recipients=recipients,
        )


@lru_cache
def get_event_service():
    return EventService()
