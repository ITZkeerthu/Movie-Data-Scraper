from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..db.connection import get_db
from ..models.movie import Movie
from ..services.scraper import fetch_wikipedia_page, parse_poster_url, parse_synopsis, parse_film_image_url
from ..services.update_service import apply_scraped_fields

router = APIRouter()


@router.post("/api/movies/{movieId}/scrape")
def scrape_movie(movieId: int = Path(...), db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movieId).first()
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie {movieId} not found")
    if not movie.release_year:
        raise HTTPException(status_code=422, detail="Movie has no release_year; cannot build Wikipedia page title")
    try:
        html = fetch_wikipedia_page(movie.title, movie.release_year)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Could not fetch Wikipedia page: {exc}")
    poster_url = parse_poster_url(html)
    synopsis = parse_synopsis(html)
    film_image_url = parse_film_image_url(html)
    updated_fields = apply_scraped_fields(movieId, poster_url, synopsis, film_image_url)
    return {"movieId": movieId, "status": "success", "updatedFields": updated_fields}
