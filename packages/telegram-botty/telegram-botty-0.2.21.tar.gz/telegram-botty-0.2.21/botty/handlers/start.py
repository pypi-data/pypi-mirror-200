from abc import ABC

from botty.keyboards import InlineKeyboard
from botty.triggers import StartGroupTrigger

from .command import CommandHandler


class StartHandler(CommandHandler, ABC):
    def __init__(
        self,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__("start", reply_text, reply_keyboard)


class StartGroupHandler(StartHandler):
    def get_trigger(self) -> StartGroupTrigger:
        return StartGroupTrigger()
