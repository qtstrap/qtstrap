from qtstrap import *


def run():
    # create the fundamental Qt objects
    app = BaseApplication()
    window = BaseMainWindow()

    # make everything a little easier to see
    set_font_options(window, {'setPointSize': 12})
    window.setMinimumSize(400, 300)

    # create the two widgets for our app
    label = QLabel('Hello World!', visible=False)
    button = QPushButton('Click me!')

    # create a function to use as an event handler
    def on_click():
        button.setVisible(False)
        label.setVisible(True)

    # register the handler to the event
    button.clicked.connect(on_click)

    # build a layout for our two widgets
    with CVBoxLayout(window) as layout:
        with layout.hbox(align='center') as layout:
            layout.add(label)
        layout.add(button)

    window.show() # show the window
    app.exec_() # start the Qt event loop


if __name__ == "__main__":
    run()