from telegram import InlineKeyboardButton


class UrlButton(InlineKeyboardButton):
    def __init__(self, text: str, url: str) -> None:
        super().__init__(text, url=url)
