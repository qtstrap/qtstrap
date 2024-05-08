from qtstrap.utils import Adapter
from qtpy.QtCore import Signal, QTimer


def test_adapter(qtbot):
    class SignalInterface(Adapter):
        sig = Signal()

    out = []
    original = SignalInterface()
    original.sig.connect(lambda: out.append('original'))
    
    original.sig.emit()
    assert out == ['original']
    out.clear()

    copy = original.adapter()
    copy.sig.connect(lambda: out.append('copy'))

    original.sig.emit()

    assert out == ['original', 'copy']
    out.clear()
    
    # copy.kill()
    # timer = QTimer(singleShot=True)
    # with qtbot.waitSignal(timer.timeout):
    #     timer.start(10)

    # original.sig.emit()
    # with qtbot.assertNotEmitted(copy.sig, wait=100):
    #     original.sig.emit()

    # assert out == ['original']
