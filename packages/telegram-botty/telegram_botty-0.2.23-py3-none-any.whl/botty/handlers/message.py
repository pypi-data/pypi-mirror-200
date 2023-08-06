from botty.callbacks import ReplyCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import MessageTrigger

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    def get_trigger(self) -> MessageTrigger:
        return MessageTrigger()


class MessageReplyHandler(MessageHandler):
    def __init__(
        self,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = ReplyCallback(text, keyboard)
        super().__init__(callback)
