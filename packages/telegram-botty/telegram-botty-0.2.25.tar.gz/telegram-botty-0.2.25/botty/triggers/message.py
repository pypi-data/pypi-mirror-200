from botty_core.types import PTBCallback, PTBHandler
from telegram import ext

from .update import UpdateTrigger


class MessageTrigger(UpdateTrigger):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def make_handler(self, callback: PTBCallback) -> PTBHandler:
        return ext.MessageHandler(self.filters, callback)
