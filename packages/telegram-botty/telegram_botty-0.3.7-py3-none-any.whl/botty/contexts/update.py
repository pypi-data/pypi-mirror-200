from botty_core import Callback, Chat, Context, Message, ReplyMarkup, User


class UpdateContext(Context):
    @property
    def message(self) -> Message:
        return self.effective_message

    @property
    def user(self) -> User:
        return self.effective_user

    @property
    def chat(self) -> Chat:
        return self.effective_chat

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message:
        raw = await self.message.reply(text, markup)
        return Message(raw)


UpdateCallback = Callback[UpdateContext]
