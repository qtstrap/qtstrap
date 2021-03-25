from time import time


def time_since(timestamp):
    return (time() - timestamp)


class TimeStamp:
    def __init__(self):
        self._time = time()

    def time_since(self, timestamp):
        return (time() - timestamp)

    def update(self):
        self._time = time()