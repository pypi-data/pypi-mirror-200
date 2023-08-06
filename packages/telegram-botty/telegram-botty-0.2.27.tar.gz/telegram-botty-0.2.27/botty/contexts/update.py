from botty_core import Callback, Context
from botty_core.types import Chat, Message, ReplyMarkup, User


class UpdateContext(Context):
    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message:
        raw = await self.message.reply(text, markup)
        return Message(raw)

    @property
    def message(self) -> Message:
        return self.effective_message

    @property
    def user(self) -> User:
        return self.effective_user

    @property
    def chat(self) -> Chat:
        return self.effective_chat


UpdateCallback = Callback[UpdateContext]
