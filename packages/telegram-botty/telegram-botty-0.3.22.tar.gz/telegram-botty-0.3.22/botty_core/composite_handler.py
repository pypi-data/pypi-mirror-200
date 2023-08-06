from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .ptb_types import PTBHandler


class CompositeHandler:
    def __init__(self, *handlers: PTBHandler | CompositeHandler) -> None:
        self._handlers = handlers

    def __iter__(self) -> Iterator[PTBHandler]:
        for handler in self._handlers:
            if isinstance(handler, CompositeHandler):
                yield from handler
            else:
                yield handler
