import telegram

from botty_core.ptb_types import ReplyMarkup

from .chat import Chat
from .object import TelegramObject
from .user import User


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

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        return await self.raw.reply_text(
            text,
            reply_markup=markup,  # type: ignore[arg-type]
        )

    async def edit(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message | bool:
        return await self.raw.edit_text(
            text,
            reply_markup=markup,  # type: ignore[arg-type]
        )
