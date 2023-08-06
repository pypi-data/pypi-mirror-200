from botty_core import PTBContext
from telegram import Update, ext

from botty.contexts import TextCallback, TextContext

from .message import MessageHandler


class TextHandler(ext.MessageHandler[PTBContext]):
    filters = MessageHandler.filters & ext.filters.TEXT

    def __init__(self, callback: TextCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    async def handle(self, update: Update, context: PTBContext) -> None:
        _context = TextContext(context, update)
        await self._callback(_context)
