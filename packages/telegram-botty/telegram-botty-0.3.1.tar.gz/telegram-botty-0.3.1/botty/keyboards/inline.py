from telegram import InlineKeyboardButton, InlineKeyboardMarkup

InlineButtons = list[list[InlineKeyboardButton]]


class InlineKeyboard(InlineKeyboardMarkup):
    def __init__(self, buttons: InlineButtons) -> None:
        super().__init__(buttons)
