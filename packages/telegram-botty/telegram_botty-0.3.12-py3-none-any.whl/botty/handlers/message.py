from botty_core import Handler, PTBContext
from telegram import Update, ext

from botty.contexts import MessageContext, UpdateCallback


class MessageHandler(ext.MessageHandler[PTBContext], Handler[MessageContext]):
    filters = ext.filters.UpdateType.MESSAGE

    def __init__(self, callback: UpdateCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    def make_context(self, raw: PTBContext, update: Update) -> MessageContext:
        return MessageContext(raw, update)
