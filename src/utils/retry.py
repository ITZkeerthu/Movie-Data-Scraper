import time
import random
import httpx
from functools import wraps


def is_transient_error(exc: Exception) -> bool:
    """True for errors worth retrying: network failures, 429 and 5xx responses.

    Other 4xx responses (e.g. a 404 for a missing Wikipedia page) are permanent.
    """
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        return code == 429 or code >= 500
    return True


def exponential_backoff(max_attempts: int = 3, base_delay: float = 0.5, max_delay: float = 10.0,
                        should_retry=None):
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
                    if attempts >= max_attempts or (should_retry and not should_retry(e)):
                        raise
                    delay = min(max_delay, base_delay * (2 ** (attempts - 1)))
                    # add some jitter
                    delay = delay * (0.5 + random.random() * 0.5)
                    time.sleep(delay)
        return wrapper
    return decorator
