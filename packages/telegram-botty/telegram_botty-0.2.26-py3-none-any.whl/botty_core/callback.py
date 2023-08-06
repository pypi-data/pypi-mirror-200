from abc import ABC, abstractmethod
from typing import TypeVar

import telegram

from .context import Context
from .types import Bot, PTBContext, Update

T = TypeVar("T")


class Callback(ABC):
    def __init__(self) -> None:
        self._raw_update: telegram.Update | None = None
        self._raw_context: PTBContext | None = None

    def set_context(self, update: telegram.Update, context: PTBContext) -> None:
        self._raw_update = update
        self._raw_context = context

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
    def context(self) -> Context:
        return Context(self.raw_context, self.raw_update)

    @property
    def raw_update(self) -> telegram.Update:
        return self.get_validated_field("raw_update", self._raw_update)

    @property
    def raw_context(self) -> PTBContext:
        return self.get_validated_field("raw_context", self._raw_context)

    @property
    def update(self) -> Update:
        return self.context.update

    @property
    def bot(self) -> Bot:
        return self.context.bot


class CallbackFieldError(AttributeError):
    def __init__(self, callback: Callback, field: str) -> None:
        self.callback = callback
        self.field = field

    def __str__(self) -> str:
        return f"You must set `{self.field}` for {self.callback}"
