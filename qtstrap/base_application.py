from .qt import *
import signal


class BaseApplication(QApplication):
    def __init__(self, register_ctrlc_handler=True) -> None:
        super().__init__()

        if register_ctrlc_handler:
            self.init_ctrlc_handler()

    def init_ctrlc_handler(self):
        # signal handler callback
        def ctrlc_handler(sig, frame):
            self.window.close()
            self.shutdown()
            
        # grab the keyboard interrupt signal 
        signal.signal(signal.SIGINT, ctrlc_handler)

        # empty timer callback
        def update():
            pass
        
        # create timer to force python interpreter to get some runtime
        self.timer = QTimer()
        self.timer.timeout.connect(update)
        self.timer.start(100)