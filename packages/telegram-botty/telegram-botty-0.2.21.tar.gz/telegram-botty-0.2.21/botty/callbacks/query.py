from botty_core.types import Query

from .reply import ReplyCallback


class QueryCallback(ReplyCallback):
    async def run(self) -> None:
        await super().run()
        await self.answer()

    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        return self.update.query
