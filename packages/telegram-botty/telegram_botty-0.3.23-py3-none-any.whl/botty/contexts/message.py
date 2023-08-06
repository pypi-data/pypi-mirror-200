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

    async def copy(
        self,
        message_id: int | None = None,
        chat_id: int | None = None,
    ) -> int:
        return await self.chat.copy(message_id or self.message.id, chat_id)


MessageCallback = Callback[MessageContext]
