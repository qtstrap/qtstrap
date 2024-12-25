class classproperty:
    """Convert a method into class property."""
    def __init__(self, func):
        self.fget = func

    def __get__(self, instance, owner):
        return self.fget(owner)


if __name__ == '__main__':

    class Test:
        lol = 'lol'

        @classproperty
        def lmao(self):
            return self.lol + ', lmao'

    print(Test.lol)
    print(Test.lmao)

    Test.lol = ''

    print(Test.lol)
    print(Test.lmao)
