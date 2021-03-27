from qtstrap import *


class VLine(QFrame):
    def __init__(self, parent=None, line_width=1):
        super().__init__(parent=parent)
        self.setFrameShape(QFrame.VLine)
        # expand vertically, but not horizontally
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setLineWidth(line_width)


class HLine(QFrame):
    def __init__(self, parent=None, line_width=1):
        super().__init__(parent=parent)
        self.setFrameShape(QFrame.HLine)

        # expand horizontally, but not vertically
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLineWidth(line_width)