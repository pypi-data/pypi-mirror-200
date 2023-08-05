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

Context = ext.ContextTypes.DEFAULT_TYPE
PTBHandler = ext.BaseHandler[Update, Context]  # type: ignore[misc]
KeyboardMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
ReplyMarkup = KeyboardMarkup | ReplyKeyboardRemove | ForceReply
PTBCallback = Callable[[telegram.Update, Context], Coroutine[Any, Any, None]]
