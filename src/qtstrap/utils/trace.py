from time import time


start_time = time()


def out(*args):
    """
    The print function used by the trace decorator.

    Overwrite this function to change the output behavior, eg to use logging instead of print.
    """
    print(*args)


def trace(func):
    """
    A decorator that logs registration, execution, and completion times of a function.
    """
    out(f'[{time() - start_time:.3f}] {func} registering trace')

    def new(*args, **kwargs):
        before = time() - start_time
        out(f'[{before:.3f}] {func} executing', args, kwargs)

        result = func(*args, **kwargs)

        after = time() - start_time
        out(f'[{after:.3f}] {func} done in {after - before:.3f}S, returned:', result)
        return result

    return new


if __name__ == '__main__':
    from time import sleep

    sleep(0.1)

    @trace
    def test(*args):
        sleep(0.1)
        print('test')
        return [*reversed(args)]

    sleep(0.1)
    test()
    test(1, 2, 3)
