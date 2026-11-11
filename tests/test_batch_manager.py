import pytest
from src.db.connection import Base, SessionLocal, engine
from src.models.batch_progress import BatchProgress
from src.models.movie import Movie
from src.services import batch_manager


@pytest.fixture(autouse=True)
def db(monkeypatch):
    monkeypatch.setattr(batch_manager.time, "sleep", lambda s: None)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    s = SessionLocal()
    s.add_all([Movie(id=1, title="A"), Movie(id=2, title="B")])
    s.commit()
    s.close()
    yield
    Base.metadata.drop_all(engine)


def _batch(batch_id):
    s = SessionLocal()
    try:
        b = s.query(BatchProgress).filter_by(batch_id=batch_id).one()
        return b.status, b.processed_records, b.last_processed_id, b.end_time
    finally:
        s.close()


def test_invalid_rate_limit_rejected():
    with pytest.raises(ValueError):
        batch_manager.start_batch(10, 0)


def test_batch_completes_and_records_progress():
    status, done, last_id, end = _batch(batch_manager.start_batch(10, 5.0))
    assert (status, done, last_id) == ("completed", 2, 2)
    assert end is not None


def test_batch_marked_failed_on_error(monkeypatch):
    def boom(_):
        raise RuntimeError("stop")
    monkeypatch.setattr(batch_manager.time, "sleep", boom)
    with pytest.raises(RuntimeError):
        batch_manager.start_batch(10, 5.0)
    s = SessionLocal()
    b = s.query(BatchProgress).one()
    assert b.status == "failed" and b.end_time is not None
    s.close()
