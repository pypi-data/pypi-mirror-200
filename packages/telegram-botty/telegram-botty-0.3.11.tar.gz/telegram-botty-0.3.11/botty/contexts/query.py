import telegram
from botty_core import Callback, Query, ReplyMarkup

from .update import UpdateContext


class QueryContext(UpdateContext):
    @property
    def query(self) -> Query:
        return self.update.query

    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    async def edit(
        self,
        text: str,
        markup: ReplyMarkup | None = None,
    ) -> telegram.Message | bool:
        return await self.message.edit(text, markup)


QueryCallback = Callback[QueryContext]
