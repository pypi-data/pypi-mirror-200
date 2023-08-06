from botty_core.types import PTBCallback, PTBHandler
from telegram import ext

from botty.buttons import CallbackButton
from botty.errors import CallbackDataError

from .update import UpdateTrigger


class QueryTrigger(UpdateTrigger):
    def __init__(self, button: CallbackButton | None = None) -> None:
        if button is None:
            callback_data = None
        else:
            callback_data = button.callback_data
            validate_callback_data(callback_data)

        self.on_callback_data = callback_data

    def make_handler(self, callback: PTBCallback) -> PTBHandler:
        return ext.CallbackQueryHandler(callback, self._filter)

    def _filter(self, callback_data: object) -> bool:
        validate_callback_data(callback_data)
        if self.on_callback_data is None:
            return True
        return callback_data == self.on_callback_data


def validate_callback_data(callback_data: object) -> None:
    if not isinstance(callback_data, str):
        raise CallbackDataError(callback_data)
