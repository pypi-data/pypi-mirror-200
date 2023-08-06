from botty_core import PTBContext
from telegram import Update, ext


class CompositeHandler(ext.ConversationHandler[PTBContext]):
    def __init__(self, *handlers: ext.BaseHandler[Update, PTBContext]) -> None:
        super().__init__(entry_points=[*handlers], states={}, fallbacks=[])
