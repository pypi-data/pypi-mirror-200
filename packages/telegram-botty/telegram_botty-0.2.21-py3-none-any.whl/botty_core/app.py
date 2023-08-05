import warnings

from telegram.constants import ParseMode
from telegram.ext import Application, Defaults
from telegram.warnings import PTBUserWarning

from .handlers import CompositeHandler

warnings.filterwarnings(
    action="ignore",
    message=".* should be built via the `ApplicationBuilder`",
    category=PTBUserWarning,
)

warnings.filterwarnings(
    action="ignore",
    message="If 'per_message=.*', 'CallbackQueryHandler'",
    category=PTBUserWarning,
)

DEFAULTS = Defaults(
    parse_mode=ParseMode.HTML,
    disable_web_page_preview=True,
)


class App:
    def __init__(self, token: str) -> None:
        builder = Application.builder()
        builder.token(token).defaults(DEFAULTS)
        builder.concurrent_updates(True)  # noqa: FBT003
        self.raw = builder.build()

    def run(self, handler: CompositeHandler) -> None:
        for subhandler in handler.build():
            self.raw.add_handler(subhandler)
        self.raw.run_polling()
