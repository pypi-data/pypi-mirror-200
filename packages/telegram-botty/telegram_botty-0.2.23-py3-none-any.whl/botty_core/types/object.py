from typing import TypeVar

import telegram

from botty_core.helpers import get_validated_field

T = TypeVar("T")


class TelegramObject:
    def __init__(self, raw: telegram.TelegramObject) -> None:
        self.raw = raw

    def get_validated_field(self, name: str, value: T | None) -> T:
        return get_validated_field(self.raw, name, value)
