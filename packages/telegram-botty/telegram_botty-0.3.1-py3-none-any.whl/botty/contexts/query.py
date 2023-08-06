from botty_core import Callback, Query

from .update import UpdateContext


class QueryContext(UpdateContext):
    @property
    def query(self) -> Query:
        return self.update.query

    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)


QueryCallback = Callback[QueryContext]
