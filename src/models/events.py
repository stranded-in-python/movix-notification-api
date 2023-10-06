from enum import Enum
from uuid import UUID

from .mixins import UserRecipientMixin


class Events(str, Enum):
    on_registration = "on_registration"
    on_subscription = "on_subscription"
    on_refund = "on_refund"


class RegistrationEvent:
    template_id: UUID = UUID(int=0)
    _vars: list[str] = [""]
    send_from: str = "welcome@movix.ru"
    subject: str = "Confirm you email"


class SubscriptionEvent:
    template_id: UUID = UUID(int=1)
    _vars: list[str] = [""]
    send_from: str = "subscription@movix.ru"
    subject: str = "Enjoy your movies!"


class RefundEvent:
    template_id: UUID = UUID(int=2)
    _vars: list[str] = [""]
    send_from: str = "refund@movix.ru"
    subject: str = "Your refund status"


class PaymentErrorEvent:
    template_id: UUID = UUID(int=3)
    _vars: list[str] = [""]
    send_from: str = "subscription@movix.ru"
    subject: str = "One more step..."


class UserOnRegistration(UserRecipientMixin):
    verification_token: str
    id_user: UUID


class UserOnSubscription(UserRecipientMixin):
    username: str
    subscription_name: str


class UserOnRefund(UserRecipientMixin):
    username: str
    amount: str


class UserOnPaymentError(UserRecipientMixin):
    username: str
    amount: str
