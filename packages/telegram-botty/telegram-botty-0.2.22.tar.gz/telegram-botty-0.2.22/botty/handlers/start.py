from botty.callbacks import TextCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import StartGroupTrigger

from .command import CommandHandler


class StartHandler(CommandHandler):
    def __init__(self, callback: TextCallback) -> None:
        super().__init__(callback, "start")


class StartReplyHandler(StartHandler):
    def __init__(
        self,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = TextCallback(text, keyboard)
        super().__init__(callback)


class StartGroupHandler(StartHandler):
    def get_trigger(self) -> StartGroupTrigger:
        return StartGroupTrigger()


class StartGroupReplyHandler(StartGroupHandler):
    def __init__(
        self,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = TextCallback(text, keyboard)
        super().__init__(callback)
