import pytest
from fastapi import HTTPException
from src.api import movies


class FakeQuery:
    def __init__(self, result): self.result = result
    def filter(self, *a): return self
    def first(self): return self.result


class FakeDB:
    def __init__(self, result): self.result = result
    def query(self, *_): return FakeQuery(self.result)


class M:
    title, release_year = "Inception", 2010


def test_scrape_unknown_movie_is_404():
    with pytest.raises(HTTPException) as e:
        movies.scrape_movie(5, db=FakeDB(None))
    assert e.value.status_code == 404


def test_scrape_uses_real_movie_title_and_year(monkeypatch):
    seen = {}
    monkeypatch.setattr(movies, "fetch_wikipedia_page", lambda t, y: seen.update(t=t, y=y) or "<p>x</p>")
    monkeypatch.setattr(movies, "apply_scraped_fields", lambda *a: ["synopsis"])
    out = movies.scrape_movie(1, db=FakeDB(M()))
    assert seen == {"t": "Inception", "y": 2010}
    assert out["updatedFields"] == ["synopsis"]


def test_scrape_missing_year_is_422():
    m = M(); m.release_year = None
    with pytest.raises(HTTPException) as e:
        movies.scrape_movie(1, db=FakeDB(m))
    assert e.value.status_code == 422


def test_fetch_failure_is_502(monkeypatch):
    def boom(*a): raise RuntimeError("down")
    monkeypatch.setattr(movies, "fetch_wikipedia_page", boom)
    with pytest.raises(HTTPException) as e:
        movies.scrape_movie(1, db=FakeDB(M()))
    assert e.value.status_code == 502
