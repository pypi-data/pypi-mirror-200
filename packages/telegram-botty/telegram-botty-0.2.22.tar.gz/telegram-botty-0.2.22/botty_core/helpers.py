from typing import TypeVar

T = TypeVar("T")


def get_validated_field(obj: object, field: str, value: T | None) -> T:
    """If `value` is None, raise `FieldError`, else return it."""
    if value is None:
        raise FieldError(obj, field)
    return value


class FieldError(AttributeError):
    def __init__(self, obj: object, field: str) -> None:
        self.obj = obj
        self.field = field

    def __str__(self) -> str:
        return f"No `{self.field}` for `{self.obj}`"
