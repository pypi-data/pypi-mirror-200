import telegram

from .object import TelegramObject


class User(TelegramObject):
    raw: telegram.User

    def __init__(self, raw: telegram.User) -> None:
        super().__init__(raw)

    @property
    def mention(self) -> str:
        return self.raw.mention_html()
