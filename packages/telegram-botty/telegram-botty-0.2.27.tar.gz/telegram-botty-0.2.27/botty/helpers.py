from typing import TypeVar

T = TypeVar("T")


def listify(obj: T) -> T | list[T]:
    """Return `[obj]` if `obj` is not a list yet."""
    if isinstance(obj, list):
        return obj
    return [obj]
