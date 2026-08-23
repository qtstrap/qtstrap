from qtstrap.utils import TimeStamp
from qtstrap.utils.call_later import call_later


def test_call_later(qtbot):
    output = []
    start = TimeStamp()

    call_later(lambda: output.append(1), 10)

    assert output == []

    qtbot.waitUntil(lambda: start.time_since() > 0.1)

    assert output == [1]