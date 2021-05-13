



def trace(func):
    print('tracing', func)
    def new(*args, **kwargs):
        print('executing', func, args, kwargs)
        func(*args, **kwargs)

    return new