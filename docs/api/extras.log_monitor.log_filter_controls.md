<!-- markdownlint-disable -->

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.log_monitor.log_filter_controls`




**Global Variables**
---------------
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **log_levels**
- **level_map**


---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerDelegate`







---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerDelegate.paint`

```python
paint(painter, option, index)
```






---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerTreeWidgetItem`




<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.__init__`

```python
__init__(parent, name, full_name)
```








---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.clicked`

```python
clicked(column)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.double_clicked`

```python
double_clicked(column)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.get_levels`

```python
get_levels()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.set_all_levels`

```python
set_all_levels(state: bool)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.set_levels`

```python
set_levels(level_filter=[])
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.update_data`

```python
update_data()
```






---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerTreeWidget`




<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.__init__`

```python
__init__()
```








---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.click`

```python
click(item, column)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.contextMenuEvent`

```python
contextMenuEvent(event)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.deselect_all`

```python
deselect_all()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L227"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.disable_all_levels`

```python
disable_all_levels(pos)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.disable_everything`

```python
disable_everything()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.double_click`

```python
double_click(item, column)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.enable_all_levels`

```python
enable_all_levels(pos)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.enable_everything`

```python
enable_everything()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.register_logger`

```python
register_logger(full_name)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L189"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.register_loggers`

```python
register_loggers(loggers)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.select_all`

```python
select_all()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L256"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.select_only`

```python
select_only(pos)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.selection_changed`

```python
selection_changed()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L209"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.set_levels_of_children`

```python
set_levels_of_children(item, state)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.set_visible_loggers`

```python
set_visible_loggers(visible_loggers)
```






---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L262"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProfileSelector`




<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.__init__`

```python
__init__()
```








---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L305"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_accept`

```python
on_accept()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L298"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_add`

```python
on_add()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L294"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_change`

```python
on_change()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_remove`

```python
on_remove()
```






---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L321"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FilterControls`




<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.__init__`

```python
__init__()
```








---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L427"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.add_profile`

```python
add_profile(name)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L440"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.change_profile`

```python
change_profile(profile_name)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L433"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.remove_profile`

```python
remove_profile(name)
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L424"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.save_settings`

```python
save_settings()
```





---

<a href="..\..\qtstrap\extras\log_monitor\log_filter_controls.py#L448"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.update_filter`

```python
update_filter()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
