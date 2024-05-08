<!-- markdownlint-disable -->

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.log_monitor.log_filter_controls`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **LOG_FILTER_COLORS**

---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_color`

```python
get_color(key)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerDelegate`







---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerDelegate.paint`

```python
paint(painter, option, index)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerTreeWidgetItem`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.__init__`

```python
__init__(parent, name, full_name)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.clicked`

```python
clicked(column)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.double_clicked`

```python
double_clicked(column)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.get_levels`

```python
get_levels()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.set_all_levels`

```python
set_all_levels(state: bool)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.set_levels`

```python
set_levels(level_filter=[])
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidgetItem.update_data`

```python
update_data()
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L132"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `LoggerTreeWidget`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.__init__`

```python
__init__()
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.click`

```python
click(item, column)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L204"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.contextMenuEvent`

```python
contextMenuEvent(event)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L259"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.deselect_all`

```python
deselect_all()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.disable_all_levels`

```python
disable_all_levels(pos)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.disable_everything`

```python
disable_everything()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L172"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.double_click`

```python
double_click(item, column)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.enable_all_levels`

```python
enable_all_levels(pos)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L222"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.enable_everything`

```python
enable_everything()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.register_logger`

```python
register_logger(full_name)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L200"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.register_loggers`

```python
register_loggers(loggers)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.select_all`

```python
select_all()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.select_only`

```python
select_only(pos)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.selection_changed`

```python
selection_changed()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.set_levels_of_children`

```python
set_levels_of_children(item, state)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `LoggerTreeWidget.set_visible_loggers`

```python
set_visible_loggers(visible_loggers)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L269"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProfileSelector`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L274"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.__init__`

```python
__init__()
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L297"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.eventFilter`

```python
eventFilter(source, event)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_accept`

```python
on_accept()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L314"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_add`

```python
on_add()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L328"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_cancel`

```python
on_cancel()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L310"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_change`

```python
on_change()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L333"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ProfileSelector.on_remove`

```python
on_remove()
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L338"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `FilterControls`




<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L363"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.__init__`

```python
__init__(table)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L452"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.add_profile`

```python
add_profile(name)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L465"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.change_profile`

```python
change_profile(profile_name)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L473"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.columns_changed`

```python
columns_changed()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L458"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.remove_profile`

```python
remove_profile(name)
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L448"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.save_settings`

```python
save_settings()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master/qtstrap/extras/log_monitor/log_filter_controls.py#L478"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `FilterControls.update_filter`

```python
update_filter()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
