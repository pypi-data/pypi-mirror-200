from botty_core.types import Query

from botty.contexts import QueryContext

from .reply import ReplyCallback


class QueryCallback(ReplyCallback):
    @property
    def context(self) -> QueryContext:
        return QueryContext(self.raw_context, self.raw_update)

    async def run(self) -> None:
        await super().run()
        await self.answer()

    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.context.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        return self.context.query
