import telegram
from botty_core import Trigger
from botty_core.types import PTBCallback, PTBHandler
from telegram import ext


class UpdateTrigger(Trigger):
    def make_handler(self, callback: PTBCallback) -> PTBHandler:
        return ext.TypeHandler(telegram.Update, callback)
