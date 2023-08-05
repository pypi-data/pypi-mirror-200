from abc import ABC, abstractmethod
from typing import TypeVar

import telegram

from botty_core.types import Bot, Context, Update

T = TypeVar("T")


class Callback(ABC):
    def __init__(self) -> None:
        self._update: Update | None = None
        self._context: Context | None = None

    def set_update(self, update: telegram.Update, context: Context) -> None:
        self._update = Update(update)
        self._context = context

    @abstractmethod
    async def run(self) -> None:
        """Execute callback."""

    async def prepare(self) -> None:  # noqa: B027
        """Called before run."""

    def get_validated_field(self, name: str, value: T | None) -> T:
        if value is None:
            raise CallbackFieldError(self, name)
        return value

    @property
    def update(self) -> Update:
        return self.get_validated_field("update", self._update)

    @property
    def context(self) -> Context:
        return self.get_validated_field("context", self._context)

    @property
    def bot(self) -> Bot:
        raw = self.context.bot
        return Bot(raw)


class CallbackFieldError(AttributeError):
    def __init__(self, callback: Callback, field: str) -> None:
        self.callback = callback
        self.field = field

    def __str__(self) -> str:
        return f"You must set `{self.field}` for {self.callback}"
