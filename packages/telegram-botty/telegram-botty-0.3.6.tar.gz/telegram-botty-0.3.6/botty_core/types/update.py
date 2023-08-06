import telegram

from .chat import Chat
from .message import Message
from .object import TelegramObject
from .query import Query
from .user import User


class Update(TelegramObject):
    raw: telegram.Update

    def __init__(self, raw: telegram.Update) -> None:
        super().__init__(raw)

    @property
    def message(self) -> Message:
        raw = self.check_field("message", self.raw.message)
        return Message(raw)

    @property
    def query(self) -> Query:
        raw = self.check_field("query", self.raw.callback_query)
        return Query(raw)

    @property
    def effective_message(self) -> Message:
        raw = self.check_field("effective_message", self.raw.effective_message)
        return Message(raw)

    @property
    def effective_chat(self) -> Chat:
        raw = self.check_field("effective_chat", self.raw.effective_chat)
        return Chat(raw)

    @property
    def effective_user(self) -> User:
        raw = self.check_field("effective_user", self.raw.effective_user)
        return User(raw)
