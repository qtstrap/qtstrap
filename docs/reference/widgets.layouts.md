<a id="widgets.layouts.*"></a>

## \*

<a id="widgets.layouts.alignments"></a>

#### alignments

<a id="widgets.layouts.orientations"></a>

#### orientations

<a id="widgets.layouts.ContextLayout"></a>

## ContextLayout Objects

```python
class ContextLayout()
```

<a id="widgets.layouts.ContextLayout.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent=None, stretch=None, margins=None, align=None, **kwargs)
```

<a id="widgets.layouts.ContextLayout.__getattr__"></a>

#### \_\_getattr\_\_

```python
def __getattr__(name)
```

<a id="widgets.layouts.ContextLayout._layout"></a>

#### \_layout

```python
@property
def _layout()
```

<a id="widgets.layouts.ContextLayout.__call__"></a>

#### \_\_call\_\_

```python
def __call__()
```

<a id="widgets.layouts.ContextLayout.add"></a>

#### add

```python
def add(item, *args, **kwargs)
```

<a id="widgets.layouts.ContextLayout.vbox"></a>

#### vbox

```python
def vbox(*args, **kwargs)
```

<a id="widgets.layouts.ContextLayout.hbox"></a>

#### hbox

```python
def hbox(*args, **kwargs)
```

<a id="widgets.layouts.ContextLayout.grid"></a>

#### grid

```python
def grid(*args, **kwargs)
```

<a id="widgets.layouts.ContextLayout.split"></a>

#### split

```python
def split(name=None, **kwargs)
```

<a id="widgets.layouts.ContextLayout.scroll"></a>

#### scroll

```python
def scroll(name=None, **kwargs)
```

<a id="widgets.layouts.ContextLayout.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

<a id="widgets.layouts.ContextLayout.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*_)
```

<a id="widgets.layouts.CVBoxLayout"></a>

## CVBoxLayout Objects

```python
class CVBoxLayout(ContextLayout, QVBoxLayout)
```

<a id="widgets.layouts.CHBoxLayout"></a>

## CHBoxLayout Objects

```python
class CHBoxLayout(ContextLayout, QHBoxLayout)
```

<a id="widgets.layouts.CGridLayout"></a>

## CGridLayout Objects

```python
class CGridLayout(ContextLayout, QGridLayout)
```

<a id="widgets.layouts.CSplitter"></a>

## CSplitter Objects

```python
class CSplitter(QSplitter)
```

<a id="widgets.layouts.CSplitter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent=None, margins=None, orientation=None, **kwargs)
```

<a id="widgets.layouts.CSplitter.add"></a>

#### add

```python
def add(item, stretch=None)
```

<a id="widgets.layouts.CSplitter.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

<a id="widgets.layouts.CSplitter.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*args)
```

<a id="widgets.layouts.PersistentCSplitter"></a>

## PersistentCSplitter Objects

```python
class PersistentCSplitter(CSplitter)
```

<a id="widgets.layouts.PersistentCSplitter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name, parent=None, **kwargs)
```

<a id="widgets.layouts.PersistentCSplitter.restore_state"></a>

#### restore\_state

```python
def restore_state()
```

<a id="widgets.layouts.PersistentCSplitter.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*args)
```

<a id="widgets.layouts.CScrollArea"></a>

## CScrollArea Objects

```python
class CScrollArea(QScrollArea)
```

<a id="widgets.layouts.CScrollArea.__init__"></a>

#### \_\_init\_\_

```python
def __init__(parent=None, margins=None, orientation=None, **kwargs)
```

<a id="widgets.layouts.CScrollArea.add"></a>

#### add

```python
def add(item, stretch=None)
```

<a id="widgets.layouts.CScrollArea.addWidget"></a>

#### addWidget

```python
def addWidget(*args, **kwargs)
```

<a id="widgets.layouts.CScrollArea.addLayout"></a>

#### addLayout

```python
def addLayout(*args, **kwargs)
```

<a id="widgets.layouts.CScrollArea.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

<a id="widgets.layouts.CScrollArea.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*args)
```

<a id="widgets.layouts.PersistentCScrollArea"></a>

## PersistentCScrollArea Objects

```python
class PersistentCScrollArea(QScrollArea)
```

<a id="widgets.layouts.PersistentCScrollArea.__init__"></a>

#### \_\_init\_\_

```python
def __init__(name, parent=None, **kwargs)
```

<a id="widgets.layouts.PersistentCScrollArea.scroll_to"></a>

#### scroll\_to

```python
def scroll_to(value)
```

<a id="widgets.layouts.PersistentCScrollArea.restore_state"></a>

#### restore\_state

```python
def restore_state()
```

<a id="widgets.layouts.PersistentCScrollArea.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*args)
```

