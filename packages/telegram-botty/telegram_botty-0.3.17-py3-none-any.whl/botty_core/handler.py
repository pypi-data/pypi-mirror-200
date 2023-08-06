from abc import ABC, abstractmethod
from typing import Generic

from telegram import Update

from .context import Callback, ContextT
from .ptb_types import PTBContext, ReturnType


class Handler(Generic[ContextT], ABC):
    _callback: Callback[ContextT]

    @abstractmethod
    def make_context(self, raw: PTBContext, update: Update) -> ContextT:
        pass

    async def handle(self, update: Update, context: PTBContext) -> ReturnType:
        _context = self.make_context(context, update)
        return await self._callback(_context)
