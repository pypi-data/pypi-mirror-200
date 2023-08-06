from botty.callbacks import ReplyCallback, ReplyCallbackKeyboard, ReplyCallbackText
from botty.triggers import MessageTrigger

from .update import UpdateHandler


class MessageHandler(UpdateHandler):
    def get_trigger(self) -> MessageTrigger:
        return MessageTrigger()


class MessageReplyHandler(MessageHandler):
    def __init__(
        self,
        text: ReplyCallbackText,
        keyboard: ReplyCallbackKeyboard = None,
    ) -> None:
        callback = ReplyCallback(text, keyboard)
        super().__init__(callback)
