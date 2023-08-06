from botty_core import Callback, Chat, Context, User


class UpdateContext(Context):
    @property
    def user(self) -> User:
        return self.effective_user

    @property
    def chat(self) -> Chat:
        return self.effective_chat


UpdateCallback = Callback[UpdateContext]
