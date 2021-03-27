# qtstrap
Like Bootstrap, but qt-er.

qtstrap is a collection of widgets, tools, and design patterns to help get your PySide2/PyQt projects up and running quickly.

# Why?

Qt is excellent, but it's also enormous. There's a lot of topics, and many of them have hidden gotchas. PySide2 and PyQt are also excellent, letting us leverage the powerful Qt libraries from up in the clouds in PythonLand, but this arrangement has its own gotchas.

The goal of qtstrap is to provide solutions to common pitfalls and usage patterns in building pyqt applications. 

# Dependencies

* Make
* Python 3.8+
* PySide2 5.15.2

# Getting Started

Creating a new qtstrap project:
```sh
> mkdir test
> cd test
> python3 -m venv .venv
> source .venv/bin/activate
> python3 -m pip install qtstrap
```

Once it's installed, running qtstrap init will prompt you for some information and then create a project skeleton in the current directory.
```
> qtstrap init
? Application Name:  TestApp
? Publisher Name:  TestAppCo
```




# Features

* qtstrap command line tool that helps bootstrap new projects
* crossplatform makefile with useful development commands
* preconfigured pyinstaller spec file
* preconfigured InnoSetup setup compiler script
* custom Qt widget subclasses with useful behaviors
  * BaseApplication
  * BaseMainWindow
* Pythonic layout system using ContextLayouts