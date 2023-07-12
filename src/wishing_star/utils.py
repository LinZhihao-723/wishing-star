import time
from math import floor


def get_current_ts() -> int:
    """
    Get the current timestamp in milliseconds from Unix epoch time.
    """
    return floor(time.time() * 1000)
