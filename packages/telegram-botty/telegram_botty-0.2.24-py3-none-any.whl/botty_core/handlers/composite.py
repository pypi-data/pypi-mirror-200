from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from botty_core.types import PTBHandler

    from .handler import Handler


class CompositeHandler:
    def __init__(self, *subhandlers: Handler | CompositeHandler) -> None:
        self.subhandlers = subhandlers

    def build(self) -> list[PTBHandler]:
        return [h.build() for h in self]

    def __iter__(self) -> Iterator[Handler]:
        for handler in self.subhandlers:
            if isinstance(handler, CompositeHandler):
                yield from handler
            else:
                yield handler
