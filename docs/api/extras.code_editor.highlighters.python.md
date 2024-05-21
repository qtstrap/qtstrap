<!-- markdownlint-disable -->

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.code_editor.highlighters.python`




**Global Variables**
---------------
- **TYPE_CHECKING**
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **STYLES**

---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format`

```python
format(color, style='')
```

Return a QTextCharFormat with the given attributes. 


---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_style`

```python
get_style(kind)
```






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PythonHighlighter`




<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.__init__`

```python
__init__(document)
```








---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.build_rules`

```python
build_rules()
```





---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.highlightBlock`

```python
highlightBlock(text)
```

Apply syntax highlighting to the given block of text. 

---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\extras\code_editor\highlighters\python.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.match_multiline`

```python
match_multiline(text, delimiter, in_state, style)
```

Do highlighting of multi-line strings. ``delimiter`` should be a ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and ``in_state`` should be a unique integer to represent the corresponding state changes when inside those strings. Returns True if we're still inside a multi-line string when this function is finished. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
