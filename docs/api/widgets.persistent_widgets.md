<!-- markdownlint-disable -->

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `widgets.persistent_widgets`




**Global Variables**
---------------
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**


---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCheckBox`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L5"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCheckBox.__init__`

```python
__init__(name, changed=None, *args, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCheckBox.restore_state`

```python
restore_state()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentLineEdit`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentLineEdit.__init__`

```python
__init__(name, *args, default='', changed=None, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentLineEdit.restore_state`

```python
restore_state()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentTextEdit`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentTextEdit.__init__`

```python
__init__(name, *args, default='', changed=None, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentTextEdit.restore_state`

```python
restore_state()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentListWidget`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentListWidget.__init__`

```python
__init__(name, items=[], default=[], changed=None, *args, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentListWidget.restore_state`

```python
restore_state()
```





---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentListWidget.selected_items`

```python
selected_items()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentTreeWidget`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentTreeWidget.__init__`

```python
__init__(
    name,
    items=[],
    index_column=0,
    default=[],
    changed=None,
    *args,
    **kwargs
)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentTreeWidget.restore_state`

```python
restore_state()
```





---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentTreeWidget.selected_items`

```python
selected_items()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentComboBox`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentComboBox.__init__`

```python
__init__(name, items=[], changed=None, *args, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentComboBox.restore_state`

```python
restore_state()
```






---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PersistentCheckableAction`




<a href="..\..\qtstrap\widgets\persistent_widgets.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCheckableAction.__init__`

```python
__init__(name, *args, **kwargs)
```








---

<a href="..\..\qtstrap\widgets\persistent_widgets.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PersistentCheckableAction.restore_state`

```python
restore_state()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
