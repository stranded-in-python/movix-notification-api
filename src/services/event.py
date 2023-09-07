import orjson

from core.config import events_properties, user_propertis
from core.exceptions import EventNameError
from models.events import UserOnRegistration
from models.queue import EmailTitle, Message, MessageType


class EventService:
    def on_registration(self, user: UserOnRegistration) -> Message:
        event_name = "on_registration"
        template_id = self._get_teplate_id(event_name)
        context = self._get_template_context(event_name, user)
        recipients = self._get_message_recipients(event_name, user)

        message = Message(
            context=context,
            template_id=template_id,
            type_=MessageType.email,
            recipients=recipients,
        )

        return message

    def _get_teplate_id(self, event_name):
        match event_name:
            case "on_registration":
                return events_properties.on_registration_id

            case _:
                raise EventNameError

    def _get_template_context(self, event_name, *args):
        match event_name:
            case "on_registration":
                return self._on_registration_context(args)

            case _:
                raise EventNameError

    def _on_registration_context(self, user: UserOnRegistration):
        context = {
            "verefy_url": user_propertis.url_verify,
            "verification_token": user.verification_token,
        }
        return orjson.dumps(context)

    def _get_message_recipients(self, event_name, *args):
        match event_name:
            case "on_registration":
                return self._on_registration_recipients(args)

            case _:
                raise EventNameError

    def _on_registration_recipients(self, user: UserOnRegistration):
        return EmailTitle(
            to_=user.email,
            from_=events_properties.on_registration_send_from,
            subject_=events_properties.on_registration_subject,
        )


def get_event_service():
    return EventService()
