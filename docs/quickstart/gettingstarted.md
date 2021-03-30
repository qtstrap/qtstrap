# Getting Started

After installing qtstrap and creating a new project using `qtstrap init`, the first thing you should do is familiarize yourself with the [qtstrap project structure](../structure/structure.md).

This will create a project skeleton in your current directory.


## `main.py`
```py
from application import Application


def run():
    app = Application() # Create the Qt Application
    app.exec_() # Run the main Qt loop


if __name__ == "__main__":
    run()
```

`main.py` is the entry point into your application. It contains the function `run()` which creates an instance of `Application` and starts the Qt event loop with `.exec_()`.

If you want to do anything before starting Qt, it belongs here in `run()`. Examples could be installing custom logging handlers or checking for updates.

## `application.py`

```py
from qtstrap import *
from main_window import MainWindow


class Application(BaseApplication):    
    def __init__(self) -> None:
        super().__init__()

        self.window = MainWindow() # create window
        self.window.show() # open it
```

`application.py` is where your customized `QApplication` lives. Here, we create an instance of `MainWindow` and open it. Any kind of long running or singleton modules or subsystems can be initialized here, where they'll live for the lifetime of the QApplication. `BaseApplication` has several useful behaviors that can read about [here](baseapplication.md).


## `main_window.py`

```py
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

```

`main_window.py` is where your application's MainWindow is defined.