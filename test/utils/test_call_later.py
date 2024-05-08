from qtstrap.utils import TimeStamp
from qtstrap.utils.call_later import call_later, _call_timers


def test_call_later(qtbot):
    output = []
    start = TimeStamp()

    assert _call_timers == []

    call_later(lambda: output.append(1), 10)

    assert output == []
    assert len(_call_timers) == 1

    qtbot.waitUntil(lambda: start.time_since() > 0.1)

    assert output == [1]
    assert _call_timers == []
