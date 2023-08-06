from botty.callbacks import ReplyCallback, ReplyCallbackKeyboard, ReplyCallbackText
from botty.triggers import TextTrigger

from .update import UpdateHandler


class TextHandler(UpdateHandler):
    def get_trigger(self) -> TextTrigger:
        return TextTrigger()


class TextReplyHandler(TextHandler):
    def __init__(
        self,
        text: ReplyCallbackText,
        keyboard: ReplyCallbackKeyboard = None,
    ) -> None:
        callback = ReplyCallback(text, keyboard)
        super().__init__(callback)
