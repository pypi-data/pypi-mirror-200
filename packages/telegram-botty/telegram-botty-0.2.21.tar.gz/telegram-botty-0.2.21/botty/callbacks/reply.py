import telegram
from botty_core import Callback
from botty_core.types import Chat, Message, ReplyMarkup, User

from botty.keyboards import InlineKeyboard


class ReplyCallback(Callback):
    def __init__(
        self,
        text: str | None = None,
        keyboard: InlineKeyboard | None = None,
    ) -> None:
        super().__init__()
        self.reply_text = text
        self.reply_keyboard = keyboard

    async def run(self) -> None:
        text = self.get_reply_text()
        if text:
            markup = self.get_reply_markup()
            await self.reply(text, markup)

    def get_reply_text(self) -> str | None:
        return self.reply_text

    def get_reply_markup(self) -> ReplyMarkup | None:
        keyboard = self.get_reply_keyboard()
        return None if keyboard is None else keyboard.build()

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        return await self.message.reply(text, markup)

    def get_reply_keyboard(self) -> InlineKeyboard | None:
        return self.reply_keyboard

    @property
    def message(self) -> Message:
        raw = self.get_validated_field("message", self.update.raw.effective_message)
        return Message(raw)

    @property
    def user(self) -> User:
        raw = self.get_validated_field("user", self.update.raw.effective_user)
        return User(raw)

    @property
    def chat(self) -> Chat:
        raw = self.get_validated_field("chat", self.update.raw.effective_chat)
        return Chat(raw)
