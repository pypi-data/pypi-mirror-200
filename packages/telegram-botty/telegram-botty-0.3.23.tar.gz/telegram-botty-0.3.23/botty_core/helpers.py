from typing import TypeVar

ObjectT = TypeVar("ObjectT", bound=object)


def check_field(owner: object, field: str, value: ObjectT | None) -> ObjectT:
    """If `value` is None, raise `FieldError`, else return it."""
    if value is None:
        raise FieldError(owner, field)
    return value


class FieldError(AttributeError):
    def __init__(self, obj: object, field: str) -> None:
        self.obj = obj
        self.field = field

    def __str__(self) -> str:
        return f"No `{self.field}` for `{self.obj}`"
