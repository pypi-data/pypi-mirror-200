from abc import abstractmethod
from typing import TypeVar

from botty_core.types import PTBHandler

T = TypeVar("T")


class Handler:
    @abstractmethod
    def build(self) -> PTBHandler:
        """Return PTB-compatible handler."""

    def get_validated_field(self, name: str, value: T | None) -> T:
        if value is None:
            raise HandlerFieldError(self, name)
        return value


class HandlerFieldError(AttributeError):
    def __init__(self, handler: Handler, field: str) -> None:
        self.handler = handler
        self.field = field

    def __str__(self) -> str:
        return f"You must set `{self.field}` for {self.handler}"
