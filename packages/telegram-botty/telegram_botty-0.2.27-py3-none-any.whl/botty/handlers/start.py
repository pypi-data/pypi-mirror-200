from telegram import ext

from botty.contexts import TextCallback

from .command import CommandHandler


class StartHandler(CommandHandler):
    def __init__(self, callback: TextCallback) -> None:
        super().__init__("start", callback)


class StartGroupHandler(StartHandler):
    filters = StartHandler.filters & ext.filters.ChatType.GROUPS
