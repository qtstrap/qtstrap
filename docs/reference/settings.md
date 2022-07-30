<a id="settings.sys"></a>

## sys

<a id="settings.uncache"></a>

#### uncache

```python
def uncache(exclude)
```

Remove package modules from cache except excluded ones.
On next import they will be reloaded.

Args:
    exclude (iter<str>): Sequence of module paths.

