# Welcome to qtstrap's documentation

qtstrap is a framework that helps you skip over the boring and tedious parts of developing applications with PySide2/PyQt. 

# Features

- `qtstrap` command line tool to bootstrap new projects
- crossplatform makefile with useful development commands
- preconfigured pyinstaller spec file
- preconfigured InnoSetup setup compiler script
- custom Qt widgets with useful behaviors
- Pythonic layout system using ContextLayouts
- light/dark theme with application-level theme switching
- `extras`:
  - CommandPalette, like VSCode or SublimeText
  - Logging Subsystem: log to local database + log viewer widgets
  - CodeEditor: Custom QTextEditor subclass customized for code editing
- Some other stuff I haven't remembered yet

## Widget types

- Buttons:
  - StateButton
  - IconToggleButton
  - ConfirmToggleButton
  - MenuButton
- LabelEdit
- HLine and VLine
- LinkLabel
- Persistent Widgets (for rapid prototyping of saved data)
  - PersistentCheckableAction
  - PersistentCheckBox
  - PersistentComboBox
  - PersistentLineEdit
  - PersistentListWidget
  - PersistentPlainTextEdit
  - PersistentTabWidget
  - PersistentTextEdit
  - PersistentTreeWidget

## Utility Classes and Functions
- Adapter
- SignalBlocker
- TimeStamp
- StringBuilder
- call_later()
- decorators:
  - @accepts_file_drops()
  - @trace
  - @singleton
- context managers:
  - Defer

# Roadmap

- Write documentation for ContextLayouts
- Create a sane menu bar constructor
- Create an application auto-updater
- Create an application crash reporter
- Set up CI/CD
- Add 'Qt principles' section