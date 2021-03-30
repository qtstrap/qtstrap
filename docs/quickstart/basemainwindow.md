# BaseMainWindow

`BaseMainWindow` is a subclass of `QMainWindow`, adding several behaviors that address shortcomings of the Qt/PySide2/PyQt environment.

# Window Icon

The `BaseMainWindow` will look for an icon file at `resources/application.ico` and automatically set it as the window icon, if it finds it. This icon is also used when packaging your application for distribution.

qtstrap ships with a default icon you can use until you create your own.

# Window Settings

A `BaseMainWindow` will stay where you put it, even when you close and and reopen your app.

`BaseMainWindow` has a pair of methods, `.save_settings()` and `.load_settings()`, that will save and restore the window's geometry(it's size and position) and it's state(minimized/maximized, etc). `.load_settings()` is automatically called when starting the application, and `.save_settings()` is automatically called when closing it. 