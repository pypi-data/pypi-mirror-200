from abc import abstractmethod

from .types import PTBCallback, PTBHandler


class Trigger:
    @abstractmethod
    def make_handler(self, callback: PTBCallback) -> PTBHandler:
        """Return PTB-compatible handler."""
