from botty_core import PTBContext
from telegram import Update, ext

from botty.buttons import CallbackButton
from botty.contexts import QueryCallback, QueryContext


class QueryHandler(ext.CallbackQueryHandler[PTBContext]):
    def __init__(self, button: CallbackButton, callback: QueryCallback) -> None:
        self._button = button
        self._callback = callback
        super().__init__(self.handle, self._filter)

    async def handle(self, update: Update, context: PTBContext) -> None:
        _context = QueryContext(context, update)
        await self._callback(_context)
        await _context.answer()

    def _filter(self, callback_data: object) -> bool:
        return callback_data == self._button.callback_data
