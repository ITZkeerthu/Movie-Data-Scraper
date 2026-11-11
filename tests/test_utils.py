import httpx
import pytest
from src.utils import http_client, retry


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(retry.time, "sleep", lambda s: None)


def test_retry_succeeds_after_transient_failures():
    calls = []

    @retry.exponential_backoff(max_attempts=3)
    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("transient")
        return "ok"

    assert flaky() == "ok"
    assert len(calls) == 3


def test_retry_raises_after_max_attempts():
    calls = []

    @retry.exponential_backoff(max_attempts=2)
    def always_fails():
        calls.append(1)
        raise ValueError("nope")

    with pytest.raises(ValueError):
        always_fails()
    assert len(calls) == 2


def test_retry_delay_is_capped(monkeypatch):
    delays = []
    monkeypatch.setattr(retry.time, "sleep", delays.append)

    @retry.exponential_backoff(max_attempts=6, base_delay=1.0, max_delay=2.0)
    def fail():
        raise RuntimeError

    with pytest.raises(RuntimeError):
        fail()
    assert len(delays) == 5 and all(d <= 2.0 for d in delays)


def test_client_throttles_between_requests(monkeypatch):
    sleeps = []
    monkeypatch.setattr(http_client.time, "sleep", sleeps.append)
    c = http_client.RateLimitedClient(rate_limit=2.0)
    c._client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, text="hi")))
    assert c.get("https://example.org/a").text == "hi"
    assert sleeps == []  # first request is never throttled
    c.get("https://example.org/b")
    assert len(sleeps) == 1 and 0 < sleeps[0] <= 0.5


def test_client_raises_on_http_error():
    c = http_client.RateLimitedClient(rate_limit=1000)
    c._client = httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(404)))
    with pytest.raises(httpx.HTTPStatusError):
        c.get("https://example.org/missing")
