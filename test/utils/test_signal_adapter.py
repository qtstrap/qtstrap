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
    copy.kill()

    original.sig.emit()

    assert out == ['original']
