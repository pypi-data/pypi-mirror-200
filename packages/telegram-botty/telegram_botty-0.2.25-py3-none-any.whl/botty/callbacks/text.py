from botty.contexts import TextContext

from .reply import ReplyCallback


class TextCallback(ReplyCallback):
    @property
    def context(self) -> TextContext:
        return TextContext(self.raw_context, self.raw_update)

    @property
    def text(self) -> str:
        return self.context.text

    @property
    def text_words(self) -> list[str]:
        return self.context.text_words
