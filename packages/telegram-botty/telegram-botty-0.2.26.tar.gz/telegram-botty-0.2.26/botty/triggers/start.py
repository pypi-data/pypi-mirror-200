from telegram import ext

from .command import CommandTrigger


class StartTrigger(CommandTrigger):
    def __init__(self) -> None:
        super().__init__("start")


class StartGroupTrigger(StartTrigger):
    filters = StartTrigger.filters & ext.filters.ChatType.GROUPS
