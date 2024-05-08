from time import time


class TimeStamp:
    """A TimeStamp object that can be used to track the time since it was created."""

    def __init__(self) -> None:
        self._time = time()

    def time_since(self) -> float:
        """Calculate the elapsed time since this TimeStamp was created or updated."""
        return time() - self._time

    def update(self) -> None:
        """Update the TimeStamp to the current time."""
        self._time = time()

    def __repr__(self) -> str:
        return str(self._time)


def time_since(timestamp: TimeStamp | float) -> float:
    """Calculate the elapsed time since the given TimeStamp or time value."""
    if isinstance(timestamp, TimeStamp):
        return time() - timestamp._time
    else:
        return time() - timestamp
