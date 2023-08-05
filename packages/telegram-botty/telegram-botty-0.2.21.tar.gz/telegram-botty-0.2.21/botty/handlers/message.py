from botty.callbacks import ReplyCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import MessageTrigger

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    def __init__(
        self,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__()
        self._reply_text = reply_text
        self._reply_keyboard = reply_keyboard

    def get_trigger(self) -> MessageTrigger:
        return MessageTrigger()

    def get_callback(self) -> ReplyCallback:
        return ReplyCallback(self._reply_text, self._reply_keyboard)
