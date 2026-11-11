from ..db.connection import SessionLocal
from ..models.movie import Movie
from ..models.batch_progress import BatchProgress
from ..services.queries import get_missing_data_movies
from sqlalchemy import func
from sqlalchemy.orm import Session
import uuid
import time


def start_batch(batch_size: int, rate_limit: float):
    if rate_limit <= 0:
        raise ValueError("rate_limit must be greater than 0")
    db: Session = SessionLocal()
    batch_id = str(uuid.uuid4())
    try:
        movies = get_missing_data_movies(db, batch_size)
        batch = BatchProgress(
            batch_id=batch_id,
            total_records=len(movies),
            processed_records=0,
            status="running"
        )
        db.add(batch)
        db.commit()
        try:
            for movie in movies:
                # Placeholder for actual scraping and update logic
                time.sleep(1.0 / rate_limit)
                batch.processed_records += 1
                batch.last_processed_id = movie.id
                db.commit()
            batch.status = "completed"
        except Exception:
            # Don't leave the batch stuck in "running" forever.
            db.rollback()
            batch.status = "failed"
            raise
        finally:
            batch.end_time = func.current_timestamp()
            db.commit()
    finally:
        db.close()
    return batch_id
