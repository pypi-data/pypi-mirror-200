from botty_core import Callback

from .update import UpdateContext


class TextContext(UpdateContext):
    @property
    def text(self) -> str:
        return self.message.text

    @property
    def text_words(self) -> list[str]:
        return self.text.lower().split()


TextCallback = Callback[TextContext]
