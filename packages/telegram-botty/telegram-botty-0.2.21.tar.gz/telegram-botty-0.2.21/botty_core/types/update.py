import telegram

from .message import Message
from .object import TelegramObject
from .query import Query


class Update(TelegramObject):
    raw: telegram.Update

    def __init__(self, raw: telegram.Update) -> None:
        super().__init__(raw)

    @property
    def message(self) -> Message:
        raw = self.get_validated_field("message", self.raw.message)
        return Message(raw)

    @property
    def query(self) -> Query:
        raw = self.get_validated_field("query", self.raw.callback_query)
        return Query(raw)
