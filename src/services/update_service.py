from ..db.connection import SessionLocal
from ..models.movie import Movie
from ..models.update_log import UpdateLog
from sqlalchemy.orm import Session


def apply_scraped_fields(movie_id: int, poster_url: str = None, synopsis: str = None, film_image_url: str = None):
    """Store scraped values on a movie and record the outcome in update_logs.

    Returns False if the movie does not exist, otherwise the list of updated
    field names (empty when the scraper found nothing; nothing is written then).
    The session is always closed and rolled back on failure.
    """
    db: Session = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            return False
        updates = {
            "poster_url": poster_url,
            "synopsis": synopsis,
            "film_image_url": film_image_url,
        }
        updated_fields = [name for name, value in updates.items() if value]
        if not updated_fields:
            return updated_fields
        try:
            for name in updated_fields:
                setattr(movie, name, updates[name])
            db.add(movie)
            db.add(UpdateLog(movie_id=movie_id, operation_type="update", status="success", retry_count=0))
            db.commit()
        except Exception as exc:
            db.rollback()
            db.add(UpdateLog(movie_id=movie_id, operation_type="update", status="failed",
                             error_message=str(exc)[:1000], retry_count=0))
            db.commit()
            raise
        return updated_fields
    finally:
        db.close()
