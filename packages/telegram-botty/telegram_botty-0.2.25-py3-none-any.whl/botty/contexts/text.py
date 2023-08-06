from .reply import ReplyContext


class TextContext(ReplyContext):
    @property
    def text(self) -> str:
        return self.message.text

    @property
    def text_words(self) -> list[str]:
        return self.text.lower().split()
