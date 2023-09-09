from typing import Callable


class Builder:
    """
    Utility class for incrementally building strings.
    """

    def __init__(
        self,
        out: Callable[[str], None] | None = None,
        indent: int = 4,
        endl: str = '\n',
    ):
        self.items = []
        if out:
            self.out = out
        else:
            self.out = self.items.append
        self.indent = indent
        self.level = 0
        self.endl = endl

    def __iadd__(self, string: str):
        self.line(string)
        return self

    def __lshift__(self, string: str) -> None:
        self.line(string)

    def line(self, string: str = ''):
        if string:
            self.out(' ' * self.indent * self.level + string + self.endl)
        else:
            self.out(self.endl)

    def join(self, base: str = ''):
        return base.join(self.items)

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, *_):
        self.level -= 1
