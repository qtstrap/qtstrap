<!-- markdownlint-disable -->

<a href="../../qtstrap/utils/adapter.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.adapter`






---

<a href="../../qtstrap/utils/adapter.py#L10"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Adapter`
A signal adapter that helps create disposable connections between objects. 

A signal-based interface can be defined using an Adapter. 

Passing an existing Adapter when creating a new Adapter will automatically link all of the existing adapter's signals to the same-named signals on the new Adapter. 

This will allow some other object to connect to these signals for whatever purpose, and then simply delete the new Adapter object when it now longer wants to recieve signals. 

Technically, Qt Signals already have a .disconnect() method, but I've never gotten it work reliably. Using an Adapter essentially gives you a nuclear .disconnect(). 

<a href="../../qtstrap/utils/adapter.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Adapter.__init__`

```python
__init__(other=None)
```








---

<a href="../../qtstrap/utils/adapter.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Adapter.adapter`

```python
adapter()
```





---

<a href="../../qtstrap/utils/adapter.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Adapter.kill`

```python
kill()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
