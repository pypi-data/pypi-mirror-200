from abc import ABC, abstractmethod
from copy import deepcopy

import telegram
from botty_core import Callback, Handler
from botty_core.types import Context, PTBHandler, Update

from botty.triggers import UpdateTrigger


class UpdateHandler(Handler, ABC):
    def __init__(self) -> None:
        self._update: Update | None = None
        self._context: Context | None = None

    def build(self) -> PTBHandler:
        return self.get_trigger().make_handler(self.handle)

    def get_trigger(self) -> UpdateTrigger:
        return UpdateTrigger()

    async def handle(self, update: telegram.Update, context: Context) -> None:
        callback = deepcopy(self.get_callback())
        callback.set_update(update, context)
        await callback.prepare()
        await callback.run()

    @abstractmethod
    def get_callback(self) -> Callback:
        pass
