from copy import deepcopy

import telegram
from botty_core import Callback, Handler
from botty_core.types import Context, PTBHandler

from botty.triggers import UpdateTrigger


class UpdateHandler(Handler):
    def __init__(self, callback: Callback) -> None:
        self._callback = callback
        self._trigger = self.get_trigger()

    def get_trigger(self) -> UpdateTrigger:
        return UpdateTrigger()

    def build(self) -> PTBHandler:
        return self._trigger.make_handler(self.handle)

    async def handle(self, update: telegram.Update, context: Context) -> None:
        callback = deepcopy(self._callback)
        callback.set_update(update, context)
        await callback.prepare()
        await callback.run()
