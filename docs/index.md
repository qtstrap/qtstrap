# Welcome to qtstrap's documentation

qtstrap is a framework that helps you skip over the boring and tedious parts of developing applications with PySide6/PyQt. 

# Features

- `qtstrap` command line tool to bootstrap new projects
- crossplatform makefile with useful development commands
- preconfigured pyinstaller spec file
- preconfigured InnoSetup setup compiler script
- Pythonic layout system using ContextLayouts
- light/dark theme with application-level theme switching
- Some other stuff I haven't remembered yet

# Custom Widgets

- LabelEdit
- HLine and VLine
- LinkLabel
 
## Buttons:
  - StateButton
  - IconToggleButton
  - ConfirmToggleButton
  - MenuButton

## Persistent Widgets (for rapid prototyping of saved data)
- PersistentCheckableAction
- PersistentCheckBox
- PersistentComboBox
- PersistentLineEdit
- PersistentListWidget
- PersistentPlainTextEdit
- PersistentTabWidget
- PersistentTextEdit
- PersistentTreeWidget

# Utility Classes and Functions
- Adapter
- TimeStamp
- StringBuilder
- call_later()

## decorators:
- @accepts_file_drops
- @trace
- @singleton

## context managers:
- Defer
- SignalBlocker

# qtstrap.extras:
  - CommandPalette, like VSCode or SublimeText
  - Logging Subsystem: log to local database + log viewer widgets
  - CodeEditor: Custom QTextEditor subclass customized for code editing

# Roadmap

- Write documentation for ContextLayouts
- Create a sane menu bar constructor
- Create an application auto-updater
- Create an application crash reporter
- Set up CI/CD
- Add 'Qt principles' section