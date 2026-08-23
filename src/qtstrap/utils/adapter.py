from qtstrap import QObject

try:
    from qtstrap import SignalInstance
except Exception:
    from qtstrap import pyqtBoundSignal as SignalInstance


class Adapter(QObject):
    """A signal adapter that helps create disposable connections between objects.

    A signal-based interface can be defined using an Adapter.

    Passing an existing Adapter when creating a new Adapter will automatically link all of
    the existing adapter's signals to the same-named signals on the new Adapter.

    This will allow some other object to connect to these signals for whatever purpose, and
    then simply call kill() when it no longer wants to receive signals.

    Connections are stored as QMetaObject.Connection objects so kill() can disconnect
    them explicitly. Signal-to-signal doesn't work here because Adapter.__call__
    interferes with PySide6's connect resolution.
    """

    def __init__(self, other=None):
        super().__init__()
        self._other = other
        self._connections = []
        if other is None:
            self._original = True
            return
        self._original = False

        for name in self._get_signals(other):
            conn = getattr(other, name).connect(getattr(self, name).emit)
            self._connections.append(conn)

    def _get_signals(self, obj):
        signals = []
        for name in dir(obj):
            if name not in dir(QObject):
                if isinstance(getattr(obj, name), SignalInstance):
                    signals.append(name)
        return signals

    def __str__(self):
        s = ''
        if not self._original:
            s += 'inherited '
        s += f"{self.__class__.__name__}(Adapter): <{', '.join(self._get_signals(self))}>"
        return s

    def __call__(self):
        return self.__class__(self)

    def adapter(self):
        return self.__class__(self)

    def kill(self):
        """Disconnect all adapter connections. The adapter stops receiving
        signals but the object itself remains valid."""
        if self._other:
            for conn in self._connections:
                self._other.disconnect(conn)
            self._connections.clear()


if __name__ == '__main__':
    from qtstrap import Signal

    class SignalInterface(Adapter):
        sig = Signal()

    original = SignalInterface()
    original.sig.connect(lambda: print('original'))

    copy = original.adapter()
    copy.sig.connect(lambda: print('copy'))

    original.sig.emit()

    copy.kill()

    original.sig.emit()

    print(original)
    print(copy)