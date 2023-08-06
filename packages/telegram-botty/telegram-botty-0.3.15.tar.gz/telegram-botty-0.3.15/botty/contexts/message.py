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
            message_id: int | None = None,
    ) -> int:
        raw = await self.bot.raw.copy_message(
            chat_id=chat_id or self.chat.id,
            from_chat_id=self.chat.id,
            message_id=message_id or self.message.id,
        )
        return raw.message_id


MessageCallback = Callback[MessageContext]
