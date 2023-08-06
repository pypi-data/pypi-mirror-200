from collections.abc import Callable, Coroutine
from typing import Any

import telegram
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
KeyboardMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
ReplyMarkup = KeyboardMarkup | ReplyKeyboardRemove | ForceReply
PTBCallback = Callable[[telegram.Update, PTBContext], Coroutine[Any, Any, None]]
