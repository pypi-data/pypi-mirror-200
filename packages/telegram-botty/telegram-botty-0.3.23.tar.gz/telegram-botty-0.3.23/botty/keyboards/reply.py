from collections.abc import Sequence

from telegram import KeyboardButton, ReplyKeyboardMarkup

ButtonRow = Sequence[str | KeyboardButton]


class ReplyKeyboard(ReplyKeyboardMarkup):
    buttons: Sequence[ButtonRow]

    def __init__(self, *buttons: ButtonRow) -> None:
        super().__init__(buttons or self.buttons, resize_keyboard=True)
