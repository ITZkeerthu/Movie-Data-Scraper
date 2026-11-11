import pytest
from src.db.connection import Base, SessionLocal, engine
from src.models.movie import Movie
from src.models.update_log import UpdateLog
from src.services import update_service


@pytest.fixture(autouse=True)
def db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    s = SessionLocal()
    s.add(Movie(id=1, title="Inception", release_year=2010))
    s.commit()
    s.close()
    yield
    Base.metadata.drop_all(engine)


def _logs():
    s = SessionLocal()
    try:
        return [(l.status, l.movie_id) for l in s.query(UpdateLog).all()]
    finally:
        s.close()


def test_unknown_movie_returns_false():
    assert update_service.apply_scraped_fields(99, synopsis="x") is False
    assert _logs() == []


def test_updates_only_provided_fields_and_logs_success():
    out = update_service.apply_scraped_fields(1, poster_url="https://x/p.jpg", synopsis="Plot")
    assert out == ["poster_url", "synopsis"]
    s = SessionLocal()
    m = s.query(Movie).get(1)
    assert (m.poster_url, m.synopsis, m.film_image_url) == ("https://x/p.jpg", "Plot", None)
    s.close()
    assert _logs() == [("success", 1)]


def test_nothing_scraped_writes_no_log():
    assert update_service.apply_scraped_fields(1) == []
    assert _logs() == []
