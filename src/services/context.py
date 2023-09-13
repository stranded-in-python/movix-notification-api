import abc
import enum
import typing
import uuid

from models.notifications import GroupedContext, Notification, UserContext
from models.users import User
from services import user as user_service


async def get_users(user_ids: typing.Iterable[uuid.UUID]) -> typing.Iterable[User]:
    service = user_service.get_service()
    return await service.get_users(user_ids)


class ContextHandlerBase(abc.ABC):
    def __init__(self, mode: str, users_context: dict[uuid.UUID, UserContext]):
        self.mode = mode
        self.users_context = users_context

    @abc.abstractmethod
    async def handle(user_ids: typing.Iterable[uuid.UUID]):
        # Do smth
        ...

    def get_context(self) -> typing.Iterable[UserContext]:
        return self.users_context.values()


class ContextHandlerUser(ContextHandlerBase):
    async def handle(self, user_ids: typing.Iterable[uuid.UUID]):
        users = await get_users(user_ids)
        if not users:
            return

        for user in users:
            user_context = self.users_context.get(uuid.UUID(user.id))

            if not user_context:
                continue

            for key in user_context.context.keys():
                match key:
                    case "first_name":
                        user_context.context[key] = user.first_name


class ContextHandlerChainBase(abc.ABC):
    def __init__(self, mode: str, handlers: typing.Iterable[type[ContextHandlerBase]]):
        self.mode = mode
        self.handlers = handlers
        self.users_context = dict()

    async def before_chain_execution(self):
        # Do smth before chain execution
        ...

    async def after_chain_execution(self):
        # Do smth after chain execution
        ...

    async def handle(
        self, context_vars: typing.Iterable[str], user_ids: typing.Iterable[uuid.UUID]
    ):
        await self.before_chain_execution()

        for handler in self.handlers:
            handler_obj: ContextHandlerBase = handler(self.mode, self.users_context)
            await handler_obj.handle(user_ids)  # type: ignore

        await self.after_chain_execution()

    async def get_context(self) -> typing.Iterable[UserContext]:
        return self.users_context.values()


class ContextHandlerChain(ContextHandlerChainBase):
    ...


class ContextBase(abc.ABC):
    context: typing.Iterable

    def __init__(
        self, notification: Notification, user_ids: typing.Iterable[uuid.UUID]
    ):
        self.notification = notification
        self.user_ids = user_ids

    def hash_context(self, context: UserContext) -> str:
        ...

    async def resolve_context(self) -> typing.Iterable[GroupedContext]:
        """Go to each variable handler"""
        ...


class Context(ContextBase):
    def __init__(
        self, notification: Notification, user_ids: typing.Iterable[uuid.UUID]
    ):
        self.notification = notification
        self.user_ids = user_ids

    def hash_context(self, context: UserContext) -> str:
        return str([item for item in context.context.items()])

    async def resolve_context(self) -> typing.Iterable[GroupedContext]:
        """Go to each variable handler"""
        if self.notification is None:
            return

        mode, handlers = get_chain_mode_by_notification(notification=self.notification)
        chain = ContextHandlerChain(mode, handlers)
        await chain.handle(self.notification.context_vars, self.user_ids)

        # В этот момент контекст это структура [{user_id: [context_var1, context_var2, ...]}, {user_id2: ...}]
        user_contexts: typing.Iterable[UserContext] = await chain.get_context()
        group_contexts = dict()

        # Группируем одинаковый контекст
        for context in user_contexts:
            key = self.hash_context(context)
            group_context = group_contexts.get(
                key, GroupedContext(user_ids=[], context=context.context)
            )
            group_context.user_ids.append(context.user_id)

        self.context = group_contexts.values()
        return self.context


class ContextChain(tuple[str, typing.Iterable[type[ContextHandlerBase]]], enum.Enum):
    # Возможно, в дальнейшем будет потребность вводить разные цепи обработки
    default = "default", (ContextHandlerUser,)


def get_chain_mode_by_notification(
    notification: Notification,
) -> tuple[str, typing.Iterable[type[ContextHandlerBase]]]:
    return ContextChain.default


def get_context_handler(
    notification: Notification, user_ids: typing.Iterable[uuid.UUID]
) -> Context:
    return Context(notification, user_ids)


async def get_context_handler_dependency():
    return get_context_handler


async def get_users_from_auth() -> list[User]:
    ...
