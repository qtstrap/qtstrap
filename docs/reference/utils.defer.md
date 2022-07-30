<a id="utils.defer.Defer"></a>

## Defer Objects

```python
class Defer()
```

A context manager that emulates the defer keyword from other languages.

The deferred thing can be any callable, and arbitrary args and kwargs will be preserved
and passed to the thing during __exit__().

<a id="utils.defer.Defer.__init__"></a>

#### \_\_init\_\_

```python
def __init__(thing, *args, **kwargs)
```

<a id="utils.defer.Defer.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__()
```

<a id="utils.defer.Defer.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(*_)
```

