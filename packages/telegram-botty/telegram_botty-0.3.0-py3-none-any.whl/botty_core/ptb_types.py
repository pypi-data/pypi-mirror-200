from collections.abc import Awaitable, Callable

from telegram import (
    ForceReply,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    ext,
)

PTBContext = ext.ContextTypes.DEFAULT_TYPE
PTBHandler = ext.BaseHandler[Update, PTBContext]  # type: ignore[misc]
PTBCallback = Callable[[Update, PTBContext], Awaitable[None]]
KeyboardMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
ReplyMarkup = KeyboardMarkup | ReplyKeyboardRemove | ForceReply
