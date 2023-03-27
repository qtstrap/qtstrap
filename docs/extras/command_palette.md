# Command Palette


Like VSCode/Sublime Text, but in your application.


## Features:
- Register `Command`s from anywhere in your application
- Supports qtstrap's global light/dark mode


## As an input method
Call `CommandPalette.open()` to open the palette as a highly configurable input method.

It supports:
- prompt text
- placeholder text
- a list of options
- a completion model
- an input validator
- an input mask

The user's input or selection is returned to you via a callback.


Installing the `CommandPalette` and defining `Command`s:


```py
from qtstrap import *
from qtstrap.extras.command_palette import CommandPalette, Command


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.command_palette = CommandPalette(self)
        
        self.commands = [
            Command('Quit Application', triggered=self.close, shortcut='Ctrl+Q'),
            Command('Theme: Set to Light Mode', triggered=lambda: App().change_theme('light')),
            Command('Theme: Set to Dark Mode', triggered=lambda: App().change_theme('dark')),
        ]
```