from collections.abc import Mapping

from botty.buttons import CallbackButton
from botty.contexts import QueryCallback

from .composite import CompositeHandler
from .query import QueryHandler


class InlineMenuHandler(CompositeHandler):
    def __init__(self, handlers: Mapping[CallbackButton, QueryCallback]) -> None:
        subhandlers = [
            QueryHandler(button, handler) for button, handler in handlers.items()
        ]
        super().__init__(*subhandlers)
