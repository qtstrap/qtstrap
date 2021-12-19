from time import time


def time_since(timestamp):
    return (time() - timestamp)


class TimeStamp:
    def __init__(self):
        self._time = time()

    def time_since(self, timestamp=None):
        if timestamp is None:
            return time() - self._time
            
        if type(timestamp) == TimeStamp():
            return time() - timestamp._time

        return time() - timestamp

    def update(self):
        self._time = time()

    def __repr__(self):
        return str(self._time)