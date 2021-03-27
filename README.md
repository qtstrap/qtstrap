# qtstrap
Like Bootstrap, but qt-er.

qtstrap is a collection of widgets, tools, and design patterns to help get your PySide2/PyQt projects up and running quickly.

# Why?

Qt is excellent, but it's also enormous. There's a lot of topics, and many of them have hidden gotchas. PySide2 and PyQt are also excellent, letting us leverage the powerful Qt libraries from up in the clouds in PythonLand, but this arrangement has its own gotchas.

The goal of qtstrap is to provide solutions to common pitfalls and usage patterns in building pyqt applications. 

# Dependencies

* Make
* Python 3.8+

# Installation

Creating a new qtstrap project:
```sh
> mkdir test
> cd test
> python3 -m venv .venv
> source .venv/bin/activate
> python3 -m pip install qtstrap
> qtstrap init
```

The init script will prompt you to enter the name of your application and the name of its publisher(which is probably you), and then it will generate an application skeleton. At this point you can deactivate the virtual environment and forget it exists(until you need to add a package or something).

You can test that everything installed properly by executing:
```
make run
```
If everything installed properly you should see something like this:

![screenshot](screenshot1.png) 

# Features

* qtstrap command line tool to bootstrap new projects
* crossplatform makefile with useful development commands
* preconfigured pyinstaller spec file
* preconfigured InnoSetup setup compiler script
* custom Qt widget subclasses with useful behaviors
  * BaseApplication
  * BaseMainWindow
  * And More!
* Pythonic layout system using ContextLayouts
* Some other stuff I haven't remembered yet