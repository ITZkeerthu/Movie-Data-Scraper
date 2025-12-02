from ..models.movie import Movie
from sqlalchemy.orm import Session

def get_missing_data_movies(db: Session, limit: int = 100):
    return db.query(Movie).filter((Movie.poster_url == None) | (Movie.film_image_url == None)).limit(limit).all()
