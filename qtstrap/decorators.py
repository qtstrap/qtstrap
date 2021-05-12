
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def trace(func):
    print('tracing', func)
    def new(*args, **kwargs):
        print('executing', func, args, kwargs)
        func(*args, **kwargs)

    return new