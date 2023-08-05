from abc import ABC

from botty.keyboards import InlineKeyboard
from botty.triggers import CommandTrigger

from .text import TextHandler


class CommandHandler(TextHandler, ABC):
    def __init__(
        self,
        command: str,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__(reply_text, reply_keyboard)
        self._command = command

    def get_trigger(self) -> CommandTrigger:
        return CommandTrigger(self._command)
