from botty_core import Handler, PTBContext
from telegram import Update, ext

from botty.contexts import TextCallback, TextContext

from .message import MessageHandler


class TextHandler(ext.MessageHandler[PTBContext], Handler[TextContext]):
    filters = MessageHandler.filters & ext.filters.TEXT

    def __init__(self, callback: TextCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    def make_context(self, raw: PTBContext, update: Update) -> TextContext:
        return TextContext(raw, update)
