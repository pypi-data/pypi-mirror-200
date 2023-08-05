from telegram import ext

from .message import MessageTrigger


class TextTrigger(MessageTrigger):
    filters = MessageTrigger.filters & ext.filters.TEXT
