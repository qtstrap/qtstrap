


class SignalBlocker:
    """ A context manager that blocks the signals of the provided widget.
    
    The signals are unblocked at the end of the with block.
    """
    def __init__(self, widget):
        self.widget = widget

    def __enter__(self):
        self.widget.blockSignals(True)

    def __exit__(self, *_):
        self.widget.blockSignals(False)