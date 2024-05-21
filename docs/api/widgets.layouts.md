<!-- markdownlint-disable -->

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `widgets.layouts`




**Global Variables**
---------------
- **alignments**
- **orientations**


---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L80"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ContextLayoutBase`







---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayoutBase.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ContextLayout`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QMainWindow | PySide6.QtWidgets.QSplitter | PySide6.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    align: Optional[Literal[<AlignmentFlag.AlignLeft: 1>, <AlignmentFlag.AlignRight: 2>, <AlignmentFlag.AlignTop: 32>, <AlignmentFlag.AlignBottom: 64>, <AlignmentFlag.AlignCenter: 132>, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ContextLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CVBoxLayout`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QMainWindow | PySide6.QtWidgets.QSplitter | PySide6.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    align: Optional[Literal[<AlignmentFlag.AlignLeft: 1>, <AlignmentFlag.AlignRight: 2>, <AlignmentFlag.AlignTop: 32>, <AlignmentFlag.AlignBottom: 64>, <AlignmentFlag.AlignCenter: 132>, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CVBoxLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CHBoxLayout`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QMainWindow | PySide6.QtWidgets.QSplitter | PySide6.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    align: Optional[Literal[<AlignmentFlag.AlignLeft: 1>, <AlignmentFlag.AlignRight: 2>, <AlignmentFlag.AlignTop: 32>, <AlignmentFlag.AlignBottom: 64>, <AlignmentFlag.AlignCenter: 132>, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CHBoxLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CGridLayout`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QMainWindow | PySide6.QtWidgets.QSplitter | PySide6.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    align: Optional[Literal[<AlignmentFlag.AlignLeft: 1>, <AlignmentFlag.AlignRight: 2>, <AlignmentFlag.AlignTop: 32>, <AlignmentFlag.AlignBottom: 64>, <AlignmentFlag.AlignCenter: 132>, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.addLayout`

```python
addLayout(
    item: PySide6.QtWidgets.QLayout,
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

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L233"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.addWidget`

```python
addWidget(
    item: PySide6.QtWidgets.QWidget,
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

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CGridLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CFormLayout`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QMainWindow | PySide6.QtWidgets.QSplitter | PySide6.QtWidgets.QWidget | widgets.layouts.ContextLayoutBase | None = None,
    stretch: int | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    align: Optional[Literal[<AlignmentFlag.AlignLeft: 1>, <AlignmentFlag.AlignRight: 2>, <AlignmentFlag.AlignTop: 32>, <AlignmentFlag.AlignBottom: 64>, <AlignmentFlag.AlignCenter: 132>, 'left', 'l', 'right', 'r', 'top', 't', 'bottom', 'bot', 'b', 'center', 'c']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L283"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.add`

```python
add(
    a: Union[str, PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, tuple[str, PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout], Sequence[tuple[str, PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]], dict[str, PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    b: PySide6.QtWidgets.QWidget = None
)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.scroll`

```python
scroll(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CFormLayout.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L315"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CSplitter`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    orientation: Optional[Literal[<Orientation.Horizontal: 1>, <Orientation.Vertical: 2>, 'horizontal', 'h', 'vertical', 'v']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L352"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    stretch: int | None = None
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CSplitter.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L377"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCSplitter`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L378"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.__init__`

```python
__init__(
    name: str,
    parent: PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L352"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    stretch: int | None = None
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.form`

```python
form(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.grid`

```python
grid(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L182"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.hbox`

```python
hbox(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L389"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.restore_state`

```python
restore_state()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.split`

```python
split(name: str | None = None, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCSplitter.vbox`

```python
vbox(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L400"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CScrollArea`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L401"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.__init__`

```python
__init__(
    parent: PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    margins: PySide6.QtCore.QMargins | tuple | int | None = None,
    orientation: Optional[Literal[<Orientation.Horizontal: 1>, <Orientation.Vertical: 2>, 'horizontal', 'h', 'vertical', 'v']] = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L438"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    stretch: int = None
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L459"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.addLayout`

```python
addLayout(*args, **kwargs)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L456"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `CScrollArea.addWidget`

```python
addWidget(*args, **kwargs)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L469"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCScrollArea`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L470"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.__init__`

```python
__init__(
    name: str,
    parent: PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout | widgets.layouts.ContextLayoutBase | None = None,
    **kwargs
)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.add`

```python
add(
    item: Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]],
    *args,
    **kwargs
) → Union[PySide6.QtWidgets.QWidget, PySide6.QtWidgets.QLayout, Sequence[PySide6.QtWidgets.QWidget | PySide6.QtWidgets.QLayout]]
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L484"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.restore_state`

```python
restore_state()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\widgets\layouts.py#L481"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCScrollArea.scroll_to`

```python
scroll_to(value: int)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
