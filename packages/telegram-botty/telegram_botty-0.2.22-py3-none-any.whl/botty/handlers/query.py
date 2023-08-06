from botty.buttons import CallbackButton
from botty.callbacks import QueryCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import QueryTrigger

from .update import UpdateHandler


class QueryHandler(UpdateHandler):
    def __init__(
        self,
        callback: QueryCallback,
        button: CallbackButton | None = None,
    ) -> None:
        self._button = button
        super().__init__(callback)

    def get_trigger(self) -> QueryTrigger:
        return QueryTrigger(self._button)


class QueryReplyHandler(QueryHandler):
    def __init__(
        self,
        button: CallbackButton | None = None,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = QueryCallback(text, keyboard)
        super().__init__(callback, button)
