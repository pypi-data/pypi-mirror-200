import telegram

from .object import TelegramObject


class Chat(TelegramObject):
    raw: telegram.Chat

    def __init__(self, raw: telegram.Chat) -> None:
        super().__init__(raw)

    @property
    def is_private(self) -> bool:
        return self.raw.type == self.raw.PRIVATE

    @property
    def is_group(self) -> bool:
        return self.raw.type in [self.raw.GROUP, self.raw.SUPERGROUP]

    @property
    def id(self) -> int:  # noqa: A003
        return self.raw.id
