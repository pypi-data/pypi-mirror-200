from abc import ABC

from botty.callbacks import TextCallback
from botty.triggers import TextTrigger

from .message import MessageHandler


class TextHandler(MessageHandler, ABC):
    def get_trigger(self) -> TextTrigger:
        return TextTrigger()

    def get_callback(self) -> TextCallback:
        return TextCallback(self._reply_text, self._reply_keyboard)
