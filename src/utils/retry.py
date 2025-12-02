import time
import random
from functools import wraps


def exponential_backoff(max_attempts: int = 3, base_delay: float = 0.5, max_delay: float = 10.0):
    """Decorator for retrying a function with exponential backoff.

    Example:
        @exponential_backoff(max_attempts=3)
        def fetch():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise
                    delay = min(max_delay, base_delay * (2 ** (attempts - 1)))
                    # add some jitter
                    delay = delay * (0.5 + random.random() * 0.5)
                    time.sleep(delay)
        return wrapper
    return decorator
