# Code Editor

## `CodeEditor`

A custom `QTextEdit` with a variety of useful code editing features:
- preconfigured monospace font
- preconfigured support for autocompletions(just add a list of strings or a QAbstractItemModel)
- `ctrl + enter` signal
- surround selection with braces
- comment/uncomment selection
- duplicate selection up/down
- move selection up/down
- indent/dedent selection
  

## `CodeLine`

A `CodeEditor` that's pretending to be a `QLineEdit`.


## `PythonHighlighter`

A QSyntaxHighlighter set up to highlight python code in a rough approximation of VSCode's default Light and Dark themes. 

Supports qtstrap's global light/dark mode.