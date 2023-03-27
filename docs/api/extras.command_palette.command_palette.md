<!-- markdownlint-disable -->

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_color`

```python
get_color(key)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandRegistry`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.__init__`

```python
__init__() → None
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.execute`

```python
execute(command_name)
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.register_command`

```python
register_command(command)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Command`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.__init__`

```python
__init__(*args, **kwargs)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.used`

```python
used()
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PopupDelegate`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.__init__`

```python
__init__(parent=None)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.get_colors`

```python
get_colors()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.paint`

```python
paint(
    painter: PySide2.QtGui.QPainter,
    option: PySide2.QtWidgets.QStyleOptionViewItem,
    index: PySide2.QtCore.QModelIndex
)
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L72"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.set_prefix`

```python
set_prefix(prefix)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandModel`







---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.data`

```python
data(index: PySide2.QtCore.QModelIndex, role: int) → Any
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.index`

```python
index(row: int, column: int, parent: PySide2.QtCore.QModelIndex) → QModelIndex
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.rowCount`

```python
rowCount(parent: PySide2.QtCore.QModelIndex) → int
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.sort_commands`

```python
sort_commands(prefix)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandCompleter`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.__init__`

```python
__init__(parent=None)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.close`

```python
close()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.get_selection`

```python
get_selection()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_down`

```python
move_selection_down()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L217"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_up`

```python
move_selection_up()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L195"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.open`

```python
open()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L192"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.reset`

```python
reset()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.update_prefix`

```python
update_prefix(prefix)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
