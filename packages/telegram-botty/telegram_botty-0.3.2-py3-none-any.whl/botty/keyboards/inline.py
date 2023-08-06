from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Sequence

InlineButtons = Sequence[Sequence[InlineKeyboardButton]]


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, buttons: InlineButtons) -> None:
        super().__init__(buttons)
