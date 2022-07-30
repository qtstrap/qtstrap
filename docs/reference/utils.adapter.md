<a id="utils.adapter.QObject"></a>

## QObject

<a id="utils.adapter.SignalInstance"></a>

## SignalInstance

<a id="utils.adapter.Adapter"></a>

## Adapter Objects

```python
class Adapter(QObject)
```

A signal adapter that helps create disposable connections between objects.

A signal-based interface can be defined using an Adapter.

Passing an existing Adapter when creating a new Adapter will automatically link all of
the existing adapter's signals to the same-named signals on the new Adapter.

This will allow some other object to connect to these signals for whatever purpose, and
then simply delete the new Adapter object when it now longer wants to recieve signals.

Technically, Qt Signals already have a .disconnect() method, but I've never gotten it work
reliably. Using an Adapter essentially gives you a nuclear .disconnect().

<a id="utils.adapter.Adapter.__init__"></a>

#### \_\_init\_\_

```python
def __init__(other=None)
```

<a id="utils.adapter.Adapter._get_signals"></a>

#### \_get\_signals

```python
def _get_signals(obj)
```

<a id="utils.adapter.Adapter.__str__"></a>

#### \_\_str\_\_

```python
def __str__()
```

<a id="utils.adapter.Adapter.__call__"></a>

#### \_\_call\_\_

```python
def __call__()
```

<a id="utils.adapter.Adapter.adapter"></a>

#### adapter

```python
def adapter()
```

<a id="utils.adapter.Adapter.kill"></a>

#### kill

```python
def kill()
```

