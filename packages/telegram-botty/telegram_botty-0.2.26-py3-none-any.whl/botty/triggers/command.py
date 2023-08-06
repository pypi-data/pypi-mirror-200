from botty_core.types import PTBCallback, PTBHandler
from telegram import ext

from .text import TextTrigger


class CommandTrigger(TextTrigger):
    def __init__(self, command: str) -> None:
        self.command = command

    def make_handler(self, callback: PTBCallback) -> PTBHandler:
        return ext.CommandHandler(self.command, callback, self.filters)
