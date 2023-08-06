from __future__ import annotations

from typing import TYPE_CHECKING

from .chat import Chat
from .object import TelegramObject
from .user import User

if TYPE_CHECKING:
    import telegram

    from botty_core import ReplyMarkup


class Message(TelegramObject):
    raw: telegram.Message

    def __init__(self, raw: telegram.Message) -> None:
        super().__init__(raw)

    @property
    def user(self) -> User:
        raw = self.check_field("user", self.raw.from_user)
        return User(raw)

    @property
    def chat(self) -> Chat:
        return Chat(self.raw.chat)

    @property
    def text(self) -> str:
        return self.check_field("text", self.raw.text)

    @property
    def id(self) -> int:  # noqa: A003
        return self.raw.id

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message:
        raw = await self.raw.reply_text(
            text,
            reply_markup=markup,  # type: ignore[arg-type]
        )
        return Message(raw)

    async def edit(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message | bool:
        raw = await self.raw.edit_text(
            text,
            reply_markup=markup,  # type: ignore[arg-type]
        )
        return raw if isinstance(raw, bool) else Message(raw)

    async def copy(
        self,
        chat_id: int | None = None,
        markup: ReplyMarkup | None = None,
    ) -> int:
        raw = await self.raw.copy(
            chat_id or self.chat.id,
            reply_markup=markup,  # type: ignore[arg-type]
        )
        return raw.message_id
