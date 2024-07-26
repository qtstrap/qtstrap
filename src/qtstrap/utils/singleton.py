def singleton(class_):
    """
    Class decorator that only allows one instance to be created.

    ```
    @singleton
    class Test: ...

    assert Test() is Test() # True
    ```
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
