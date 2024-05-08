from qtstrap.utils import singleton


def test_singleton(qtbot):
    
    @singleton
    class Test:
        def __init__(self):
            pass
    
    a = Test()
    b = Test()

    assert a is b