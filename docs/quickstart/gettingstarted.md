# Getting Started

After installing qtstrap and creating a new project using `qtstrap init`, the first thing you should do is familiarize yourself with the [qtstrap project structure](../structure/structure.md).

This will create a project skeleton in your current directory.


## `main.py`
```py
from qtstrap import *
import app_info


def run():
    # create the fundamental Qt objects
    app = BaseApplication(app_info=app_info)
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
```