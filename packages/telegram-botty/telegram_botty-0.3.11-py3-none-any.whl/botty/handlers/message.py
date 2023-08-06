from botty_core import Handler, PTBContext
from telegram import Update, ext

from botty.contexts import UpdateCallback, UpdateContext


class MessageHandler(ext.MessageHandler[PTBContext], Handler[UpdateContext]):
    filters = ext.filters.UpdateType.MESSAGE

    def __init__(self, callback: UpdateCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    def make_context(self, raw: PTBContext, update: Update) -> UpdateContext:
        return UpdateContext(raw, update)
