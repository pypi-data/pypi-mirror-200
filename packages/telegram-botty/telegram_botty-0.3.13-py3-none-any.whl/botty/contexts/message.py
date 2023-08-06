from botty_core import Callback, Message, ReplyMarkup

from .update import UpdateContext


class MessageContext(UpdateContext):
    @property
    def message(self) -> Message:
        return self.effective_message

    async def reply(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message:
        return await self.message.reply(text, markup)

    async def edit(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> Message | bool:
        return await self.message.edit(text, markup)

    async def copy(
        self,
        chat_id: int | None = None,
        markup: ReplyMarkup | None = None,
    ) -> int:
        return await self.message.copy(chat_id, markup)


MessageCallback = Callback[MessageContext]
