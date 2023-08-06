from typing import cast

import telegram

from .aliases import ReplyMarkup
from .chat import Chat
from .object import TelegramObject
from .user import User


class Message(TelegramObject):
    raw: telegram.Message

    def __init__(self, raw: telegram.Message) -> None:
        super().__init__(raw)

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        markup = cast(ReplyMarkup, markup)  # fix PTB error
        return await self.raw.reply_text(text, reply_markup=markup)

    @property
    def user(self) -> User:
        raw = self.get_validated_field("user", self.raw.from_user)
        return User(raw)

    @property
    def chat(self) -> Chat:
        return Chat(self.raw.chat)

    @property
    def text(self) -> str:
        return self.get_validated_field("text", self.raw.text)
