<!-- markdownlint-disable -->

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.command_palette.command_palette`




**Global Variables**
---------------
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **registry**

---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L312"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `CommandPalette`

```python
CommandPalette(parent=None)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandRegistry`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L7"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.__init__`

```python
__init__() → None
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.execute`

```python
execute(command_name)
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandRegistry.register_command`

```python
register_command(command)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Command`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.__init__`

```python
__init__(*args, **kwargs)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Command.used`

```python
used()
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PopupDelegate`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.__init__`

```python
__init__(parent=None)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.paint`

```python
paint(
    painter: PySide6.QtGui.QPainter,
    option: PySide6.QtWidgets.QStyleOptionViewItem,
    index: PySide6.QtCore.QModelIndex
)
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PopupDelegate.set_prefix`

```python
set_prefix(prefix)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandModel`







---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.data`

```python
data(index: PySide6.QtCore.QModelIndex, role: int) → Any
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L127"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.index`

```python
index(row: int, column: int, parent: PySide6.QtCore.QModelIndex) → QModelIndex
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.rowCount`

```python
rowCount(parent: PySide6.QtCore.QModelIndex) → int
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandModel.sort_commands`

```python
sort_commands(prefix)
```






---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CommandCompleter`




<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.__init__`

```python
__init__(parent=None)
```








---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.close`

```python
close()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.get_selection`

```python
get_selection()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_down`

```python
move_selection_down()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.move_selection_up`

```python
move_selection_up()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.open`

```python
open()
```





---

<a href="..\..\qtstrap\extras\command_palette\command_palette.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CommandCompleter.update_prefix`

```python
update_prefix(prefix)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
