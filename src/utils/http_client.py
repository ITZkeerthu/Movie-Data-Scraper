import time
import httpx
from ..config.settings import settings

class RateLimitedClient:
    def __init__(self, rate_limit: float = None, timeout: float = 10.0):
        # rate_limit: requests per second
        self.rate_limit = rate_limit or settings.WIKIPEDIA_RATE_LIMIT
        self._last_request = 0.0
        self._client = httpx.Client(timeout=timeout)

    def _throttle(self):
        if self.rate_limit and self._last_request > 0:
            min_interval = 1.0 / float(self.rate_limit)
            elapsed = time.time() - self._last_request
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

    def get(self, url: str, **kwargs) -> httpx.Response:
        self._throttle()
        resp = self._client.get(url, **kwargs)
        self._last_request = time.time()
        resp.raise_for_status()
        return resp

    def close(self):
        self._client.close()

# Convenience wrapper
_default_client = None

def get_client() -> RateLimitedClient:
    global _default_client
    if _default_client is None:
        _default_client = RateLimitedClient()
    return _default_client
