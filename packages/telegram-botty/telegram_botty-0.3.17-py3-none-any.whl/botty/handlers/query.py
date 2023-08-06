from botty_core import Handler, PTBContext
from telegram import Update, ext

from botty.buttons import CallbackButton
from botty.contexts import QueryCallback, QueryContext


class QueryHandler(ext.CallbackQueryHandler[PTBContext], Handler[QueryContext]):
    def __init__(self, button: CallbackButton, callback: QueryCallback) -> None:
        self._button = button
        self._callback = callback
        super().__init__(self.handle, self._filter)

    def make_context(self, raw: PTBContext, update: Update) -> QueryContext:
        return QueryContext(raw, update)

    def _filter(self, callback_data: object) -> bool:
        return callback_data == self._button.callback_data
