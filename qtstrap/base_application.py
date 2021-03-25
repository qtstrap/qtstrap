from .qt import *
import signal


class BaseApplication(QApplication):
    def __init__(self, register_ctrlc_handler=True) -> None:
        super().__init__()

        if register_ctrlc_handler:
            self.init_ctrlc_handler()

    def ctrlc_handler(self, sig=None, frame=None):
        # give all the app's children a chance to close
        for child in self.children():
            if hasattr(child, 'close'):
                child.close()

        # TODO: should we somehow wait for our children to close?

        # tell the application to close
        self.shutdown()

    def init_ctrlc_handler(self):            
        # grab the keyboard interrupt signal 
        signal.signal(signal.SIGINT, self.ctrlc_handler)

        # empty timer callback
        def update():
            pass
        
        # create timer to force python interpreter to get some runtime
        self.timer = QTimer()
        self.timer.timeout.connect(update)
        self.timer.start(100)