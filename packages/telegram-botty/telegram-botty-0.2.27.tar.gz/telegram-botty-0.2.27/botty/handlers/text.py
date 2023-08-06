from botty_core.types import PTBContext
from telegram import Update, ext

from botty.contexts import TextCallback, TextContext

from .message import MessageHandler


class TextHandler(MessageHandler):
    filters = MessageHandler.filters & ext.filters.TEXT

    def __init__(self, callback: TextCallback) -> None:
        self._callback = callback  # type: ignore[assignment]
        # noinspection PyTypeChecker
        super().__init__(self._callback)

    async def handle(self, update: Update, _context: PTBContext) -> None:
        context = TextContext(_context, update)
        await self._callback(context)
