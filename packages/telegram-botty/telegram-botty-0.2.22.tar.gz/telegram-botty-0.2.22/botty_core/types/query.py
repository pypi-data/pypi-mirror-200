import telegram

from .message import Message
from .object import TelegramObject
from .user import User


class Query(TelegramObject):
    raw: telegram.CallbackQuery

    def __init__(self, raw: telegram.CallbackQuery) -> None:
        super().__init__(raw)

    @property
    def data(self) -> str:
        return self.get_validated_field("data", self.raw.data)

    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.raw.answer(text, show_alert)

    @property
    def message(self) -> Message:
        raw = self.get_validated_field("message", self.raw.message)
        return Message(raw)

    @property
    def user(self) -> User:
        raw = self.get_validated_field("user", self.raw.from_user)
        return User(raw)
