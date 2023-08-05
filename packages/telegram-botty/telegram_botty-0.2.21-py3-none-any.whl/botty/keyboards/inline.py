from abc import ABC, abstractmethod

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

InlineButtons = list[list[InlineKeyboardButton]]


class InlineKeyboard(ABC):
    def build(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(self.get_buttons())

    @abstractmethod
    def get_buttons(self) -> InlineButtons:
        """Return rows, where row is a list of PTB-compatible buttons."""
