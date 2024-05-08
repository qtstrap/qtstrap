# QtStrap: Qt application bootstrapping framework


[![license](https://img.shields.io/pypi/l/qtstrap.svg)](./LICENSE)
[![pypi version](https://img.shields.io/pypi/v/qtstrap.svg)](https://pypi.org/project/qtstrap/)
[![PyPI status](https://img.shields.io/pypi/status/qtstrap.svg)](https://github.com/qtstrap/qtstrap)


Qt is excellent, but it's also enormous. There's a lot of topics, and many of them have hidden gotchas. PySide2 and PyQt are also excellent, letting us leverage the powerful Qt libraries from up in the clouds in PythonLand, but this arrangement has its own gotchas. 

The goal of qtstrap is get your applications up and running quickly, so you can focus on your problem instead of on Qt's idiosyncracies.

# Features

More complete docs are available [here](https://qtstrap.github.io/).

* `qtstrap` command line tool to bootstrap new projects
* crossplatform makefile with useful development commands
* preconfigured build system using PyInstaller and InnoSetup
* custom Qt widgets with useful behaviors
* Pythonic layout system using ContextLayouts
* Some other stuff I haven't remembered yet

# Quick start

```sh
$ mkdir test && cd test
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python3 -m pip install qtstrap PySide6
$ qtstrap init
```

The init script will prompt you to enter the name of your application and the name of its publisher(which is probably you), and then it will generate an application skeleton.

You can test that everything installed properly by executing:
```sh
$ python3 app/main.py
```
If you see a window like this, then you're good to go:

![screenshot](docs/screenshot1.png) 

## Custom Widgets

- `LabelEdit`
- `HLine` and `VLine`
- `LinkLabel`
- Buttons:
  - `StateButton`
  - `IconToggleButton`
  - `ConfirmToggleButton`
  - `MenuButton`
- Persistent Widgets (for rapid prototyping of saved data):
  - `PersistentCheckableAction`
  - `PersistentCheckBox`
  - `PersistentComboBox`
  - `PersistentLineEdit`
  - `PersistentListWidget`
  - `PersistentPlainTextEdit`
  - `PersistentTabWidget`
  - `PersistentTextEdit`
  - `PersistentTreeWidget`

## Utility Classes and Functions
- `Adapter`
- `TimeStamp`
- `StringBuilder`
- `call_later()`

## decorators:
- `@accepts_file_drops`
- `@trace`
- `@singleton`

## context managers:
- `Defer`
- `SignalBlocker`

## qtstrap.extras:
  - `CommandPalette`, like VSCode or SublimeText
  - Logging Subsystem: log to local database + log viewer widgets
  - `CodeEditor`: Custom QTextEditor subclass customized for code editing


# Dependencies

* Python 3
* PySide2 or PyQt5
* Make(optional, but recommended)

# Installation

```sh 
pip install qtstrap
```

# Contributing

Contributions are always welcome. Feel free to [open an issue](https://github.com/qtstrap/qtstrap/issues/new)
or [start a new discussion](https://github.com/qtstrap/qtstrap/discussions/new) on our GitHub.
