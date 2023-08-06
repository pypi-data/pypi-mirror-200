from collections.abc import Sequence

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

ButtonRow = Sequence[InlineKeyboardButton]


class InlineKeyboard(InlineKeyboardMarkup):
    buttons: Sequence[ButtonRow]

    def __init__(self, *buttons: ButtonRow) -> None:
        super().__init__(buttons)
