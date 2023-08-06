from botty_core.types import PTBContext
from telegram import Update, ext

from botty.contexts import UpdateCallback, UpdateContext


class MessageHandler(ext.MessageHandler[PTBContext]):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def __init__(self, callback: UpdateCallback) -> None:
        self._callback = callback
        super().__init__(self.filters, self.handle)

    async def handle(self, update: Update, _context: PTBContext) -> None:
        context = UpdateContext(_context, update)
        await self._callback(context)
