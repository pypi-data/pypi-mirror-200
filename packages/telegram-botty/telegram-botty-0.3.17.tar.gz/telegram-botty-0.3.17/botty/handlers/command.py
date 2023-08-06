from collections.abc import Mapping

from botty_core import Handler, PTBContext
from telegram import Update, ext

from botty.contexts import TextCallback, TextContext

from .composite import CompositeHandler


class CommandHandler(ext.CommandHandler[PTBContext], Handler[TextContext]):
    filters: ext.filters.BaseFilter = ext.filters.UpdateType.MESSAGE

    def __init__(self, command: str, callback: TextCallback) -> None:
        self._callback = callback
        super().__init__(command, self.handle, self.filters)

    def make_context(self, raw: PTBContext, update: Update) -> TextContext:
        return TextContext(raw, update)


class CommandsHandler(CompositeHandler):
    def __init__(self, handlers: Mapping[str, TextCallback]) -> None:
        subhandlers = [
            CommandHandler(button, handler) for button, handler in handlers.items()
        ]
        super().__init__(*subhandlers)
