from ..db.connection import SessionLocal
from ..models.movie import Movie
from ..models.update_log import UpdateLog
from sqlalchemy.orm import Session


def apply_scraped_fields(movie_id: int, poster_url: str = None, synopsis: str = None, film_image_url: str = None):
    db: Session = SessionLocal()
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        db.close()
        return False
    updated_fields = []
    if poster_url:
        movie.poster_url = poster_url
        updated_fields.append("poster_url")
    if synopsis:
        movie.synopsis = synopsis
        updated_fields.append("synopsis")
    if film_image_url:
        movie.film_image_url = film_image_url
        updated_fields.append("film_image_url")
    db.add(movie)
    db.commit()
    log = UpdateLog(
        movie_id=movie_id,
        operation_type="update",
        status="success",
        retry_count=0
    )
    db.add(log)
    db.commit()
    db.close()
    return updated_fields
