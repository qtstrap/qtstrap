class Defer:
    """ A context manager that emulates the defer keyword from other languages.

    The deferred thing can be any callable, and arbitrary args and kwargs will be preserved
    and passed to the thing during __exit__().
    """

    def __init__(self, thing, *args, **kwargs):
        self.thing = thing
        self.args = args
        self.kwargs = kwargs

    def __enter__(self): ...

    def __exit__(self, *_):
        self.thing(*self.args, **self.kwargs)


if __name__ == '__main__':
    print('first')
    with Defer(lambda: print('fourth')):
        with Defer(print, 'third'):
            print('second')
