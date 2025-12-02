from sqlalchemy import Column, Integer, String, DECIMAL, Text, TIMESTAMP
from sqlalchemy.sql import func
from ..db.connection import Base

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(100))
    language = Column(String(50))
    release_year = Column(Integer)
    imdb_rating = Column(DECIMAL(3,1))
    poster_url = Column(Text)
    synopsis = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    budget_crores = Column(DECIMAL(10,2))
    gross_crores = Column(DECIMAL(10,2))
    film_image_url = Column(Text)

    def __repr__(self):
        return f"<Movie id={self.id} title={self.title!r} year={self.release_year}>"
