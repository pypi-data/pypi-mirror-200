from botty.callbacks import TextCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import TextTrigger

from .update import UpdateHandler


class TextHandler(UpdateHandler):
    def get_trigger(self) -> TextTrigger:
        return TextTrigger()


class TextReplyHandler(TextHandler):
    def __init__(
        self,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = TextCallback(text, keyboard)
        super().__init__(callback)
