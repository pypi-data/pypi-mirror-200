from collections.abc import Callable

import telegram
from botty_core import Callback
from botty_core.types import Chat, Message, ReplyMarkup, User

from botty.contexts import ReplyContext
from botty.keyboards import InlineKeyboard

TextGetter = Callable[[ReplyContext], str | None]
KeyboardGetter = Callable[[ReplyContext], InlineKeyboard | None]
ReplyCallbackText = str | TextGetter
ReplyCallbackKeyboard = InlineKeyboard | KeyboardGetter | None


class ReplyCallback(Callback):
    def __init__(
        self,
        text: ReplyCallbackText,
        keyboard: ReplyCallbackKeyboard = None,
    ) -> None:
        super().__init__()
        self.reply_text = text
        self.reply_keyboard = keyboard

    @property
    def context(self) -> ReplyContext:
        return ReplyContext(self.raw_context, self.raw_update)

    async def run(self) -> None:
        text = self.get_reply_text()
        if text:
            markup = self.get_reply_markup()
            await self.reply(text, markup)

    def get_reply_text(self) -> str | None:
        if callable(self.reply_text):
            return self.reply_text(self.context)
        return self.reply_text

    def get_reply_markup(self) -> ReplyMarkup | None:
        keyboard = self.get_reply_keyboard()
        return None if keyboard is None else keyboard.build()

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        return await self.context.reply(text, markup)

    def get_reply_keyboard(self) -> InlineKeyboard | None:
        if callable(self.reply_keyboard):
            return self.reply_keyboard(self.context)
        return self.reply_keyboard

    @property
    def message(self) -> Message:
        return self.context.effective_message

    @property
    def user(self) -> User:
        return self.context.effective_user

    @property
    def chat(self) -> Chat:
        return self.context.effective_chat
