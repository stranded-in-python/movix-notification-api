import abc
import enum
import uuid
from typing import Iterable

from models.notifications import GroupedContext, Notification, UserContext


def get_chain_mode_by_notification(notification: Notification):
    if notification:
        return ContextChain.default


class ContextHandlerBase(abc.ABC):
    def __init__(self, mode: str, users_context: dict[str, UserContext]):
        ...

    @abc.abstractmethod
    async def handle(user_ids: list[uuid.UUID]):
        # Do smth
        ...


class ContextHandlerUser(ContextHandlerBase):
    async def handle(self, user_ids: list[uuid.UUID]):
        users = await get_users_from_auth(user_ids)

        for user in users:
            user_context = self.users_context.get(user.id, [])

            for key in user_context.keys():
                match key:
                    case "first_name":
                        user_context[key] = user.first_name


class ContextHandlerChainBase(abc.ABC):
    def __init__(self, mode: str, handlers: Iterable[ContextHandlerBase]):
        self.mode = mode
        self.handlers = handlers
        self.users_context = dict()

    async def before_chain_execution(self):
        # Do smth before chain execution
        ...

    async def after_chain_execution(self):
        # Do smth after chain execution
        ...

    async def handle(self, context_vars: Iterable[str], user_ids: Iterable[uuid.UUID]):
        await self.before_chain_execution()

        async for handler in self.handlers:
            await handler(self.mode, self.users_context).handle(
                self.mode, self.users_context
            )

        await self.after_chain_execution()

    async def get_context(self):
        ...


class ContextBase(abc.ABC):
    context: list

    def __init__(self, notification: Notification, user_ids: Iterable[uuid.UUID]):
        self.notification = notification
        self.user_ids = user_ids

    def validate_context(self):
        """Go to redis, retrieve actual list of variables for context, check"""
        ...

    def hash_context(self, context: UserContext) -> str:
        ...

    async def resolve_context(self) -> Iterable[GroupedContext]:
        """Go to each variable handler"""
        ...


class Context(ContextBase):
    def __init__(self, notification: Notification, user_ids: Iterable[uuid.UUID]):
        self.notification = notification
        self.user_ids = user_ids

    def validate_context(self):
        """Go to redis, retrieve actual list of variables for context, check"""
        ...

    def hash_context(self, context: UserContext) -> str:
        return str([item for item in context.context.items()])

    async def resolve_context(self) -> Iterable[GroupedContext]:
        """Go to each variable handler"""
        chain = await get_chain_mode_by_notification(notification=self.notification)
        await chain.handle(self.notification.context_vars, self.user_ids)

        # В этот момент контекст это структура [{user_id: [context_var1, context_var2, ...]}, {user_id2: ...}]
        user_contexts: list[UserContext] = await chain.get_context()
        group_contexts = dict()

        # Группируем одинаковый контекст
        for context in user_contexts:
            key = self.hash_context(context)
            group_context = group_contexts.get(
                key, GroupedContext(ids=[], context=context.context)
            )
            group_context.ids.append(context.user_id)

        self.context = group_contexts.values()


class ContextChain(enum.Enum):
    # Возможно, в дальнейшем будет потребность вводить разные цепи обработки
    default = ("default", (ContextHandlerUser,))


def get_context_handler(
    notification: Notification, user_ids: Iterable[uuid.UUID]
) -> Context:
    return Context(notification, user_ids)


async def get_users_from_auth():
    ...
