from botty_core import PTBContext
from telegram import Update, ext

from botty.contexts import TextCallback, TextContext


class CommandHandler(ext.CommandHandler[PTBContext]):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def __init__(self, command: str, callback: TextCallback) -> None:
        self._callback = callback
        super().__init__(command, self.handle, self.filters)

    async def handle(self, update: Update, _context: PTBContext) -> None:
        context = TextContext(_context, update)
        await self._callback(context)
