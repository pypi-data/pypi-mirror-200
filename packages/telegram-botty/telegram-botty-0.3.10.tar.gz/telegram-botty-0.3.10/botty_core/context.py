from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

import telegram

from botty_core.types import Bot, Chat, Message, Update, User

from .ptb_types import PTBContext


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


ContextT = TypeVar("ContextT", bound=Context)
Callback = Callable[[ContextT], Awaitable[Any]]  # TODO
