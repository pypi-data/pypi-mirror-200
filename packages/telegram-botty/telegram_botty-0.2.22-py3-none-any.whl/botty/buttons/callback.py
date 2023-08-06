from telegram import InlineKeyboardButton


class CallbackButton(InlineKeyboardButton):
    def __init__(self, text: str, callback_data: str = "") -> None:
        callback_data = callback_data or text
        super().__init__(text, callback_data=callback_data)
