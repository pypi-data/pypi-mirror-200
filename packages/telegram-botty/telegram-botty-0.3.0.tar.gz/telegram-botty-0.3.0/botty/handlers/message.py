from botty_core import PTBContext
from telegram import Update, ext

from botty.contexts import UpdateCallback, UpdateContext


class MessageHandler(ext.MessageHandler[PTBContext]):
    filters = ext.filters.UpdateType.MESSAGE

    def __init__(self, callback: UpdateCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    async def handle(self, update: Update, context: PTBContext) -> None:
        _context = UpdateContext(context, update)
        await self._callback(_context)
