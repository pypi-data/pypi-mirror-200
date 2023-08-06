from typing import TypeVar

import telegram

from botty_core.types import Bot, Chat, Message, PTBContext, Update, User

T = TypeVar("T")


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

    def get_validated_field(self, name: str, value: T | None) -> T:
        if value is None:
            raise ContextFieldError(self, name)
        return value


class ContextFieldError(AttributeError):
    def __init__(self, context: Context, field: str) -> None:
        self.context = context
        self.field = field

    def __str__(self) -> str:
        return f"No `{self.field}` for {self.context}"
