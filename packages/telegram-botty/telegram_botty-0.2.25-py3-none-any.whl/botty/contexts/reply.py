import telegram
from botty_core import Context
from botty_core.types import Chat, Message, ReplyMarkup, User


class ReplyContext(Context):
    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message:
        return await self.message.reply(text, markup)

    @property
    def message(self) -> Message:
        return self.effective_message

    @property
    def user(self) -> User:
        return self.effective_user

    @property
    def chat(self) -> Chat:
        return self.effective_chat
