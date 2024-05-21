<!-- markdownlint-disable -->

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\utils\defer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.defer`






---

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\utils\defer.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Defer`
A context manager that emulates the defer keyword from other languages. 

The deferred thing can be any callable, and arbitrary args and kwargs will be preserved and passed to the thing during __exit__(). 

<a href="https://github.com/qtstrap/qtstrap/blob/master\qtstrap\utils\defer.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Defer.__init__`

```python
__init__(thing, *args, **kwargs)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
