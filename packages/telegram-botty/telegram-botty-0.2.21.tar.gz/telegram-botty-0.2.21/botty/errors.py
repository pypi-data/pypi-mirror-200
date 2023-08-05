class CallbackDataError(ValueError):
    def __init__(self, callback_data: object) -> None:
        self.callback_data = callback_data

    def __str__(self) -> str:
        return f"Invalid callback_data: {self.callback_data}"
