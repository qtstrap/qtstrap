<!-- markdownlint-disable -->

<a href="../../qtstrap/widgets/layouts.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `widgets.layouts`




**Global Variables**
---------------
- **alignments**
- **orientations**


---

<a href="../../qtstrap/widgets/layouts.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ContextLayoutBase`







---

<a href="../../qtstrap/widgets/layouts.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayoutBase.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```






---

<a href="../../qtstrap/widgets/layouts.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ContextLayout`




<a href="../../qtstrap/widgets/layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QMainWindow | PySide2.QtWidgets.QSplitter | PySide2.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    align: typing.Optional[typing.Literal[PySide2.QtCore.Qt.AlignmentFlag.AlignLeft, PySide2.QtCore.Qt.AlignmentFlag.AlignRight, PySide2.QtCore.Qt.AlignmentFlag.AlignTop, PySide2.QtCore.Qt.AlignmentFlag.AlignBottom, PySide2.QtCore.Qt.AlignmentFlag.AlignCenter, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L217"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CVBoxLayout`




<a href="../../qtstrap/widgets/layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QMainWindow | PySide2.QtWidgets.QSplitter | PySide2.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    align: typing.Optional[typing.Literal[PySide2.QtCore.Qt.AlignmentFlag.AlignLeft, PySide2.QtCore.Qt.AlignmentFlag.AlignRight, PySide2.QtCore.Qt.AlignmentFlag.AlignTop, PySide2.QtCore.Qt.AlignmentFlag.AlignBottom, PySide2.QtCore.Qt.AlignmentFlag.AlignCenter, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CHBoxLayout`




<a href="../../qtstrap/widgets/layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QMainWindow | PySide2.QtWidgets.QSplitter | PySide2.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    align: typing.Optional[typing.Literal[PySide2.QtCore.Qt.AlignmentFlag.AlignLeft, PySide2.QtCore.Qt.AlignmentFlag.AlignRight, PySide2.QtCore.Qt.AlignmentFlag.AlignTop, PySide2.QtCore.Qt.AlignmentFlag.AlignBottom, PySide2.QtCore.Qt.AlignmentFlag.AlignCenter, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CGridLayout`




<a href="../../qtstrap/widgets/layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QMainWindow | PySide2.QtWidgets.QSplitter | PySide2.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    align: typing.Optional[typing.Literal[PySide2.QtCore.Qt.AlignmentFlag.AlignLeft, PySide2.QtCore.Qt.AlignmentFlag.AlignRight, PySide2.QtCore.Qt.AlignmentFlag.AlignTop, PySide2.QtCore.Qt.AlignmentFlag.AlignBottom, PySide2.QtCore.Qt.AlignmentFlag.AlignCenter, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.addLayout`

```python
addLayout(
    item: PySide2.QtWidgets.QLayout,
    row: int,
    column: int,
    row_span: int = 1,
    column_span: int = 1,
    rowSpan: int = 1,
    columnSpan: int = 1,
    **kwargs
) → None
```

Change the function signature to allow using the spans as named params 

---

<a href="../../qtstrap/widgets/layouts.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.addWidget`

```python
addWidget(
    item: PySide2.QtWidgets.QWidget,
    row: int,
    column: int,
    row_span: int = 1,
    column_span: int = 1,
    rowSpan: int = 1,
    columnSpan: int = 1,
    **kwargs
) → None
```

Change the function signature to allow using the spans as named params 

---

<a href="../../qtstrap/widgets/layouts.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CFormLayout`




<a href="../../qtstrap/widgets/layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QMainWindow | PySide2.QtWidgets.QSplitter | PySide2.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    align: typing.Optional[typing.Literal[PySide2.QtCore.Qt.AlignmentFlag.AlignLeft, PySide2.QtCore.Qt.AlignmentFlag.AlignRight, PySide2.QtCore.Qt.AlignmentFlag.AlignTop, PySide2.QtCore.Qt.AlignmentFlag.AlignBottom, PySide2.QtCore.Qt.AlignmentFlag.AlignCenter, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L175"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CSplitter`




<a href="../../qtstrap/widgets/layouts.py#L271"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    orientation: typing.Optional[typing.Literal[PySide2.QtCore.Qt.Orientation.Horizontal, PySide2.QtCore.Qt.Orientation.Vertical, 'horizontal', 'h', 'vertical', 'v']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L307"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    stretch: int | None = None
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```






---

<a href="../../qtstrap/widgets/layouts.py#L332"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCSplitter`




<a href="../../qtstrap/widgets/layouts.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.__init__`

```python
__init__(
    name: str,
    parent: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L307"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    stretch: int | None = None
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.restore_state`

```python
restore_state()
```






---

<a href="../../qtstrap/widgets/layouts.py#L355"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CScrollArea`




<a href="../../qtstrap/widgets/layouts.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.__init__`

```python
__init__(
    parent: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    margins: PySide2.QtCore.QMargins | tuple | int | None = None,
    orientation: typing.Optional[typing.Literal[PySide2.QtCore.Qt.Orientation.Horizontal, PySide2.QtCore.Qt.Orientation.Vertical, 'horizontal', 'h', 'vertical', 'v']] = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L393"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    stretch: int = None
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L414"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.addLayout`

```python
addLayout(*args, **kwargs)
```





---

<a href="../../qtstrap/widgets/layouts.py#L411"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.addWidget`

```python
addWidget(*args, **kwargs)
```






---

<a href="../../qtstrap/widgets/layouts.py#L424"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCScrollArea`




<a href="../../qtstrap/widgets/layouts.py#L425"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.__init__`

```python
__init__(
    name: str,
    parent: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    **kwargs
)
```








---

<a href="../../qtstrap/widgets/layouts.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.add`

```python
add(
    item: PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout],
    *args,
    **kwargs
) → PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout | list[PySide2.QtWidgets.QWidget | PySide2.QtWidgets.QLayout]
```





---

<a href="../../qtstrap/widgets/layouts.py#L439"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.restore_state`

```python
restore_state()
```





---

<a href="../../qtstrap/widgets/layouts.py#L436"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.scroll_to`

```python
scroll_to(value: int)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
