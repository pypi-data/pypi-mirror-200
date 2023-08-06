from botty.callbacks import ReplyCallback
from botty.keyboards import InlineKeyboard
from botty.triggers import CommandTrigger

from .update import UpdateHandler


class CommandHandler(UpdateHandler):
    def __init__(self, callback: ReplyCallback, command: str) -> None:
        self._command = command
        super().__init__(callback)

    def get_trigger(self) -> CommandTrigger:
        return CommandTrigger(self._command)


class CommandReplyHandler(CommandHandler):
    def __init__(
        self,
        command: str,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        callback = ReplyCallback(text, keyboard)
        super().__init__(callback, command)
