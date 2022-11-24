from qtstrap import *


def test_defer_ctx_manager():
    out = []

    out.append(1)
    with Defer(lambda: out.append(4)):
        with Defer(out.append, 3):
            out.append(2)

    assert out == [1, 2, 3, 4]
