<!-- markdownlint-disable -->

<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `extras.code_editor.highlighters.python`




**Global Variables**
---------------
- **PYQT6**
- **PYQT5**
- **PYSIDE2**
- **PYSIDE6**
- **STYLES**

---

<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L4"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `format`

```python
format(color, style='')
```

Return a QTextCharFormat with the given attributes. 


---

<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PythonHighlighter`




<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.__init__`

```python
__init__(document)
```








---

<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L113"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.highlightBlock`

```python
highlightBlock(text)
```

Apply syntax highlighting to the given block of text.  



---

<a href="..\..\qtstrap\extras\code_editor\highlighters\python.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `PythonHighlighter.match_multiline`

```python
match_multiline(text, delimiter, in_state, style)
```

Do highlighting of multi-line strings. ``delimiter`` should be a ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and ``in_state`` should be a unique integer to represent the corresponding state changes when inside those strings. Returns True if we're still inside a multi-line string when this function is finished. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
