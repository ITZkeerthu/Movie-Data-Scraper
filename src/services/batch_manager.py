from ..db.connection import SessionLocal
from ..models.movie import Movie
from ..models.batch_progress import BatchProgress
from ..services.queries import get_missing_data_movies
from sqlalchemy.orm import Session
import uuid
import time


def start_batch(batch_size: int, rate_limit: float):
    db: Session = SessionLocal()
    batch_id = str(uuid.uuid4())
    movies = get_missing_data_movies(db, batch_size)
    batch = BatchProgress(
        batch_id=batch_id,
        total_records=len(movies),
        processed_records=0,
        status="running"
    )
    db.add(batch)
    db.commit()
    for movie in movies:
        # Placeholder for actual scraping and update logic
        time.sleep(1.0 / rate_limit)
        batch.processed_records += 1
        db.commit()
    batch.status = "completed"
    db.commit()
    db.close()
    return batch_id
