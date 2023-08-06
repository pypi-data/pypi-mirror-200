from botty_core import PTBContext, PTBHandler
from telegram import Update


class CompositeHandler(PTBHandler):
    def __init__(self, *handlers: PTBHandler) -> None:
        self._handlers = handlers
        super().__init__(self.handle)

    async def handle(self, update: Update, context: PTBContext) -> object:
        for handler in self._handlers:
            if handler.check_update(update):  # TODO
                return await handler.callback(update, context)
        return None

    def check_update(self, update: object) -> bool | PTBHandler:
        for handler in self._handlers:
            if handler.check_update(update):
                return handler
        return False
