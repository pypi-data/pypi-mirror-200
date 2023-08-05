from botty.buttons import CallbackButton
from botty.callbacks import QueryCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import QueryTrigger

from .update import UpdateHandler


class QueryHandler(UpdateHandler):
    def __init__(
        self,
        button: CallbackButton | None = None,
        reply_text: str | None = None,
        reply_keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__()
        self._button = button
        self._reply_text = reply_text
        self._reply_keyboard = reply_keyboard

    def get_trigger(self) -> QueryTrigger:
        return QueryTrigger(self._button)

    def get_callback(self) -> QueryCallback:
        return QueryCallback(self._reply_text, self._reply_keyboard)
