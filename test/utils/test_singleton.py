from qtstrap.utils import singleton


def test_singleton(qtbot):
    @singleton
    class Test: ...

    a = Test()
    b = Test()

    assert a is b
