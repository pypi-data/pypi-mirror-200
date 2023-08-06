import tomllib
from pathlib import Path


class Texts:
    def __init__(self, path: str) -> None:
        reader = Path(path).open("rb")
        self.items = tomllib.load(reader)

    def get_words(self, key: int) -> list[str]:
        text = self[key]
        return text.lower().split()

    def __getitem__(self, item: int) -> str:
        key = str(item)
        if key in self.items:
            return str(self.items[key])
        raise TextsKeyError(key)


class TextsKeyError(KeyError):
    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return f"No text with key `{self.key}`"
