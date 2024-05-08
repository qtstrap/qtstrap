<!-- markdownlint-disable -->

<a href="../../qtstrap/utils/utils.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.utils`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**

---

<a href="../../qtstrap/utils/utils.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `enable_children`

```python
enable_children(thing: PySide2.QtCore.QObject) → None
```

Recursively walk the provided thing and enable all of its widget children. 


---

<a href="../../qtstrap/utils/utils.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `disable_children`

```python
disable_children(thing: PySide2.QtCore.QObject) → None
```

Recursively walk the provided thing and disable all of its widget children. 


---

<a href="../../qtstrap/utils/utils.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_children`

```python
get_children(obj: PySide2.QtCore.QObject) → list
```

Recursively visit all the children of the specified object and collect them in a list. 


---

<a href="../../qtstrap/utils/utils.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `print_children`

```python
print_children(obj: PySide2.QtCore.QObject, prefix='') → None
```

Recursively visit all the children of the specified object and print them. 


---

<a href="../../qtstrap/utils/utils.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `set_font_options`

```python
set_font_options(obj: PySide2.QtCore.QObject, options={})
```

Set the QFont options of the specified object. Font options are specified by providing the name of the QFont setter method. 



**Example:**
 set_font_options(widget, {'setPointSize': 12, 'setBold': True}) 

is equivalent to writing: font = widget.font() font.setPointSize(12) font.setBold(True) widget.setFont(font) 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
