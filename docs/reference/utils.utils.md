<a id="utils.utils.*"></a>

## \*

<a id="utils.utils.enable_children"></a>

#### enable\_children

```python
def enable_children(thing: QObject) -> None
```

Recursively walk the provided thing and enable all of its widget children.

<a id="utils.utils.disable_children"></a>

#### disable\_children

```python
def disable_children(thing: QObject) -> None
```

Recursively walk the provided thing and disable all of its widget children.

<a id="utils.utils.get_children"></a>

#### get\_children

```python
def get_children(obj: QObject) -> list
```

Recursively visit all the children of the specified object and collect them in a list.

<a id="utils.utils.print_children"></a>

#### print\_children

```python
def print_children(obj: QObject, prefix='') -> None
```

Recursively visit all the children of the specified object and print them.

<a id="utils.utils.set_font_options"></a>

#### set\_font\_options

```python
def set_font_options(obj: QObject, options={})
```

Set the QFont options of the specified object.
Font options are specified by providing the name of the QFont setter method.

Example:
set_font_options(widget, {'setPointSize': 12, 'setBold': True})

is equivalent to writing:
font = widget.font()
font.setPointSize(12)
font.setBold(True)
widget.setFont(font)

