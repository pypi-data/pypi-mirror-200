from collections.abc import Awaitable, Callable
from typing import TypeVar

import telegram

from .helpers import ObjectT, check_field
from .ptb_types import AnyDict, PTBContext, ReturnType
from .types import Bot, Chat, Message, Update, User


class Context:
    def __init__(self, raw: PTBContext, update: telegram.Update) -> None:
        self.raw = raw
        self.update = Update(update)

    @property
    def bot(self) -> Bot:
        raw = self.raw.bot
        return Bot(raw)

    @property
    def effective_message(self) -> Message:
        return self.update.effective_message

    @property
    def effective_chat(self) -> Chat:
        return self.update.effective_chat

    @property
    def effective_user(self) -> User:
        return self.update.effective_user

    @property
    def storage(self) -> AnyDict:
        return self.check_field("storage", self.raw.chat_data)

    def check_field(self, name: str, value: ObjectT | None) -> ObjectT:
        return check_field(self.raw, name, value)


ContextT = TypeVar("ContextT", bound=Context)
Callback = Callable[[ContextT], Awaitable[ReturnType]]
