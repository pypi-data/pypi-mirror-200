from botty.buttons import CallbackButton
from botty.callbacks import ReplyCallback, ReplyCallbackKeyboard, ReplyCallbackText
from botty.triggers import QueryTrigger

from .update import UpdateHandler


class QueryHandler(UpdateHandler):
    def __init__(
        self,
        callback: ReplyCallback,
        button: CallbackButton,
    ) -> None:
        self._button = button
        super().__init__(callback)

    def get_trigger(self) -> QueryTrigger:
        return QueryTrigger(self._button)


class QueryReplyHandler(QueryHandler):
    def __init__(
        self,
        button: CallbackButton,
        text: ReplyCallbackText,
        keyboard: ReplyCallbackKeyboard = None,
    ) -> None:
        callback = ReplyCallback(text, keyboard)
        super().__init__(callback, button)
