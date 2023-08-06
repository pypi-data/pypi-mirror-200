from botty_core import Callback
from botty_core.types import Query

from .update import UpdateContext


class QueryContext(UpdateContext):
    async def answer(self, text: str = "", *, show_alert: bool = False) -> bool:
        return await self.query.answer(text, show_alert=show_alert)

    @property
    def query(self) -> Query:
        return self.update.query


QueryCallback = Callback[QueryContext]
