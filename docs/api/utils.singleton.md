<!-- markdownlint-disable -->

<a href="../../qtstrap/utils/singleton.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `utils.singleton`





---

<a href="../../qtstrap/utils/singleton.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `singleton`

```python
singleton(class_)
```

Class decorator that only allows one instance to be created. 

```
@singleton
class Test: ...

assert Test() is Test() # True
``` 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
