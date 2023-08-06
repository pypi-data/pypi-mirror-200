import telegram

from botty_core.helpers import ObjectT, check_field


class TelegramObject:
    def __init__(self, raw: telegram.TelegramObject) -> None:
        self.raw = raw

    def check_field(self, name: str, value: ObjectT | None) -> ObjectT:
        return check_field(self.raw, name, value)
