<!-- markdownlint-disable -->

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.command_palette.command_palette`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **COMMAND_PALETTE_COLORS**
- **registry**

---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_color`

```python
get_color(key)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandRegistry`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.__init__`

```python
__init__() → None
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.execute`

```python
execute(command_name)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.register_command`

```python
register_command(command)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Command`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.__init__`

```python
__init__(*args, **kwargs)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.used`

```python
used()
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PopupDelegate`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.__init__`

```python
__init__(parent=None)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.get_colors`

```python
get_colors()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.paint`

```python
paint(
    painter: PySide2.QtGui.QPainter,
    option: PySide2.QtWidgets.QStyleOptionViewItem,
    index: PySide2.QtCore.QModelIndex
)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.set_prefix`

```python
set_prefix(prefix)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandModel`







---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.data`

```python
data(index: PySide2.QtCore.QModelIndex, role: int) → Any
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.index`

```python
index(row: int, column: int, parent: PySide2.QtCore.QModelIndex) → QModelIndex
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.rowCount`

```python
rowCount(parent: PySide2.QtCore.QModelIndex) → int
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.sort_commands`

```python
sort_commands(prefix)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandCompleter`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.__init__`

```python
__init__(parent=None)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.close`

```python
close()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.get_selection`

```python
get_selection()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_down`

```python
move_selection_down()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_up`

```python
move_selection_up()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.open`

```python
open()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L198"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.reset`

```python
reset()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/command_palette/command_palette.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.update_prefix`

```python
update_prefix(prefix)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
