<a id="qtstrap"></a>

# qtstrap

<a id="qtstrap.base_application"></a>

# qtstrap.base\_application

<a id="qtstrap.base_window"></a>

# qtstrap.base\_window

<a id="qtstrap.extras.code_editor.code_editor"></a>

# qtstrap.extras.code\_editor.code\_editor

<a id="qtstrap.extras.code_editor.code_line"></a>

# qtstrap.extras.code\_editor.code\_line

<a id="qtstrap.extras.code_editor.highlighters.python"></a>

# qtstrap.extras.code\_editor.highlighters.python

<a id="qtstrap.extras.code_editor.highlighters.python.format"></a>

#### format

```python
def format(color, style='')
```

Return a QTextCharFormat with the given attributes.

<a id="qtstrap.extras.code_editor.highlighters.python.PythonHighlighter"></a>

## PythonHighlighter Objects

```python
class PythonHighlighter(QSyntaxHighlighter)
```

Syntax highlighter for the Python language.

<a id="qtstrap.extras.code_editor.highlighters.python.PythonHighlighter.highlightBlock"></a>

#### highlightBlock

```python
def highlightBlock(text)
```

Apply syntax highlighting to the given block of text.

<a id="qtstrap.extras.code_editor.highlighters.python.PythonHighlighter.match_multiline"></a>

#### match\_multiline

```python
def match_multiline(text, delimiter, in_state, style)
```

Do highlighting of multi-line strings. ``delimiter`` should be a
``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and
``in_state`` should be a unique integer to represent the corresponding
state changes when inside those strings. Returns True if we're still
inside a multi-line string when this function is finished.

<a id="qtstrap.extras.code_editor.highlighters"></a>

# qtstrap.extras.code\_editor.highlighters

<a id="qtstrap.extras.code_editor"></a>

# qtstrap.extras.code\_editor

<a id="qtstrap.extras.command_palette.command_palette"></a>

# qtstrap.extras.command\_palette.command\_palette

<a id="qtstrap.extras.command_palette"></a>

# qtstrap.extras.command\_palette

<a id="qtstrap.extras.log_monitor.log_database_handler"></a>

# qtstrap.extras.log\_monitor.log\_database\_handler

<a id="qtstrap.extras.log_monitor.log_database_handler.DatabaseHandler"></a>

## DatabaseHandler Objects

```python
class DatabaseHandler(logging.Handler)
```

<a id="qtstrap.extras.log_monitor.log_database_handler.DatabaseHandler.callbacks"></a>

#### callbacks

A logging.Handler subclass that redirects outbound records to a local sqlite3 database

<a id="qtstrap.extras.log_monitor.log_filter_controls"></a>

# qtstrap.extras.log\_monitor.log\_filter\_controls

<a id="qtstrap.extras.log_monitor.log_profile"></a>

# qtstrap.extras.log\_monitor.log\_profile

<a id="qtstrap.extras.log_monitor.log_table_view"></a>

# qtstrap.extras.log\_monitor.log\_table\_view

<a id="qtstrap.extras.log_monitor.log_widget"></a>

# qtstrap.extras.log\_monitor.log\_widget

<a id="qtstrap.extras.log_monitor"></a>

# qtstrap.extras.log\_monitor

<a id="qtstrap.extras.style.colors"></a>

# qtstrap.extras.style.colors

<a id="qtstrap.extras.style.dark_palette"></a>

# qtstrap.extras.style.dark\_palette

<a id="qtstrap.extras.style"></a>

# qtstrap.extras.style

<a id="qtstrap.extras"></a>

# qtstrap.extras

<a id="qtstrap.options"></a>

# qtstrap.options

<a id="qtstrap.qt"></a>

# qtstrap.qt

<a id="qtstrap.settings"></a>

# qtstrap.settings

<a id="qtstrap.settings.uncache"></a>

#### uncache

```python
def uncache(exclude)
```

Remove package modules from cache except excluded ones.
On next import they will be reloaded.

**Arguments**:

- `exclude` _iter<str>_ - Sequence of module paths.

<a id="qtstrap.template.app.main"></a>

# qtstrap.template.app.main

<a id="qtstrap.toolbar"></a>

# qtstrap.toolbar

<a id="qtstrap.utils.adapter"></a>

# qtstrap.utils.adapter

<a id="qtstrap.utils.adapter.Adapter"></a>

## Adapter Objects

```python
class Adapter(QObject)
```

A signal adapter that helps create disposable connections between objects.

A signal-based interface can be defined using an Adapter.

Passing an existing Adapter when creating a new Adapter will automatically link all of
the existing adapter's signals to the same-named signals on the new Adapter.

This will allow some other object to connect to these signals for whatever purpose, and
then simply delete the new Adapter object when it now longer wants to recieve signals.

Technically, Qt Signals already have a .disconnect() method, but I've never gotten it work
reliably. Using an Adapter essentially gives you a nuclear .disconnect().

<a id="qtstrap.utils.decorators"></a>

# qtstrap.utils.decorators

<a id="qtstrap.utils.defer"></a>

# qtstrap.utils.defer

<a id="qtstrap.utils.defer.Defer"></a>

## Defer Objects

```python
class Defer()
```

A context manager that emulates the defer keyword from other languages.

The deferred thing can be any callable, and arbitrary args and kwargs will be preserved
and passed to the thing during __exit__().

<a id="qtstrap.utils.signals"></a>

# qtstrap.utils.signals

<a id="qtstrap.utils.signals.SignalBlocker"></a>

## SignalBlocker Objects

```python
class SignalBlocker()
```

A context manager that blocks the signals of the provided widget.

The signals are unblocked at the end of the with block.

<a id="qtstrap.utils.singleton"></a>

# qtstrap.utils.singleton

<a id="qtstrap.utils.singleton.singleton"></a>

#### singleton

```python
def singleton(class_)
```



<a id="qtstrap.utils.timestamp"></a>

# qtstrap.utils.timestamp

<a id="qtstrap.utils.utils"></a>

# qtstrap.utils.utils

<a id="qtstrap.utils.utils.enable_children"></a>

#### enable\_children

```python
def enable_children(thing: QObject) -> None
```

Recursively walk the provided thing and enable all of its widget children.

<a id="qtstrap.utils.utils.disable_children"></a>

#### disable\_children

```python
def disable_children(thing: QObject) -> None
```

Recursively walk the provided thing and disable all of its widget children.

<a id="qtstrap.utils.utils.get_children"></a>

#### get\_children

```python
def get_children(obj: QObject) -> list
```

Recursively visit all the children of the specified object and collect them in a list.

<a id="qtstrap.utils.utils.print_children"></a>

#### print\_children

```python
def print_children(obj: QObject, prefix='') -> None
```

Recursively visit all the children of the specified object and print them.

<a id="qtstrap.utils.utils.set_font_options"></a>

#### set\_font\_options

```python
def set_font_options(obj: QObject, options={})
```

Set the QFont options of the specified object.
Font options are specified by providing the name of the QFont setter method.

**Example**:

  set_font_options(widget, {'setPointSize': 12, 'setBold': True})
  
  is equivalent to writing:
  font = widget.font()
  font.setPointSize(12)
  font.setBold(True)
  widget.setFont(font)

<a id="qtstrap.utils"></a>

# qtstrap.utils

<a id="qtstrap.version"></a>

# qtstrap.version

<a id="qtstrap.widgets.buttons"></a>

# qtstrap.widgets.buttons

<a id="qtstrap.widgets.labeledit"></a>

# qtstrap.widgets.labeledit

<a id="qtstrap.widgets.layouts"></a>

# qtstrap.widgets.layouts

<a id="qtstrap.widgets.line_widgets"></a>

# qtstrap.widgets.line\_widgets

<a id="qtstrap.widgets.link_label"></a>

# qtstrap.widgets.link\_label

<a id="qtstrap.widgets.persistent_tab_widget"></a>

# qtstrap.widgets.persistent\_tab\_widget

<a id="qtstrap.widgets.persistent_widgets"></a>

# qtstrap.widgets.persistent\_widgets

<a id="qtstrap.widgets"></a>

# qtstrap.widgets

<a id="qtstrap.__main__"></a>

# qtstrap.\_\_main\_\_

