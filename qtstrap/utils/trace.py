from time import time


start_time = time()


def trace(func):
    print(f'[{time() - start_time:.3f}] tracing', func)

    def new(*args, **kwargs):
        print(f'[{time() - start_time:.3f}] executing', func, args, kwargs)
        return func(*args, **kwargs)

    return new