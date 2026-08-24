instances = {}


def singleton(class_):
    """
    Class decorator that only allows one instance to be created.

    ```
    @singleton
    class Test: ...

    assert Test() is Test() # True
    ```
    """

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    # Mark the raw class so other systems (e.g. StatusBar auto-discovery)
    # can find the wrapper after decoration.
    class_._singleton_wrapper = getinstance
    return getinstance
