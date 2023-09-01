class Builder:
    """
    Utility class for incrementally building strings.
    """

    def __init__(self, out=None, indent=4):
        self.items = []
        if out:
            self.out = out
        else:
            self.out = self.items.append
        self.indent = indent
        self.level = 0

    def __lshift__(self, item):
        self.line(item)

    def line(self, string=''):
        if string:
            self.out(' ' * self.indent * self.level + string + '\n')
        else:
            self.out('\n')

    def join(self, base: str):
        return base.join(self.items)

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, *_):
        self.level -= 1
