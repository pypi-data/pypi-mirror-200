import os


class Env:
    def __init__(self) -> None:
        self._vars = os.environ

    def get(self, var: str) -> str:
        if var in self._vars:
            return self._vars[var]
        raise EnvError(var)


env = Env()


class EnvError(KeyError):
    def __init__(self, var: str) -> None:
        self.var = var

    def __str__(self) -> str:
        return f"You must set `{self.var}` environment variable"
