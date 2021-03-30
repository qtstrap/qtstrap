# BaseApplication

`BaseApplication` is a subclass of `QApplication`, adding several behaviors that address shortcomings of the Qt/PySide2/PyQt environment.

# Ctrl+C Handler

Due to the way that the thin layer of python interacts with the Qt libraries underneath, a naked PySide2/PyQt application can't be stopped using ctrl+c like a normal program. I find this extremely annoying. 

The solution to this has two parts. Part 1 is to use the python `signal` library to bind a function to the SIGINT signal. Unfortunately, this isn't enough, because in order for signal handler to fire, the python interpreter needs to get some cpu time. Once you start the Qt interpreter using `app.exec_()`, execution passes down into Qt's C++ code and doesn't return until the application exits. Thus, we need to artifically secure some runtime for the python interpreter.

This is part 2: creating a `QTimer` that triggers every 10ms(the exact time is not important) and calls an empty python function, `update()`. When the timer triggers and `update()` is called, execution is passed back to the python interpreter, giving it a chance to process signals. 

```py
def init_ctrlc_handler(self):            
    # grab the keyboard interrupt signal 
    signal.signal(signal.SIGINT, self.ctrlc_handler)

    # empty timer callback
    def update():
        pass
    
    # create timer to force python interpreter to get some runtime
    self.timer = QTimer() # create a QTimer
    self.timer.timeout.connect(update) # connect to our empty timer callback
    self.timer.start(10) # set the timer to trigger every 10mS
```

# App Info

Several Qt modules can automatically query the running `QApplication` for a number of attributes:

- organizationName
- organizationDomain
- applicationName
- applicationVersion

One example is `QSettings`, which "provides persistent, platform-independent application settings". Using `QSettings` reqires an applicationName and an organizationName. 

```py
# every time you want to access QSettings, yuck
settings = QSettings('Organization', 'Application')
```

However, if you give this information to your `QApplication`, then `QSettings` will use those values so you don't have to specify them every time.

```py
# once, at startup
app = QApplication()
app.setOrganizationName('Organization')
app.setApplicationName('Application')

# every time you want to access QSettings, much better!
settings = QSettings()
```

As a side bonus, a `QMainWindow` will automatically set its window title attribute to the `QApplication`'s `applicationName`.