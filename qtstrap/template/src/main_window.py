from qtstrap import *


class MainWindow(BaseMainWindow):
    def __init__(self):
        super().__init__()

        set_font_options(self, {'setPointSize': 12})
        self.setMinimumSize(400, 300)

        self.label = QLabel('Hello World!')
        self.button = QPushButton('Click me!', clicked=self.on_click)

        with CVBoxLayout(self) as layout:
            with layout.hbox(align='center') as layout:
                layout.add(self.label)
            layout.add(self.button)

        self.label.setVisible(False)

    def on_click(self):
        self.button.setVisible(False)
        self.label.setVisible(True)
