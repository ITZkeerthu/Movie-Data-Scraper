from fastapi import APIRouter, Path
from ..services.scraper import fetch_wikipedia_page, parse_poster_url, parse_synopsis, parse_film_image_url
from ..services.update_service import apply_scraped_fields

router = APIRouter()

@router.post("/api/movies/{movieId}/scrape")
def scrape_movie(movieId: int = Path(...)):
    # For demo: fetch movie from DB, get title/year, scrape Wikipedia
    # Here, you would fetch the movie record and use its title/year
    # For now, use placeholder values
    title = "Inception"
    year = 2010
    html = fetch_wikipedia_page(title, year)
    poster_url = parse_poster_url(html)
    synopsis = parse_synopsis(html)
    film_image_url = parse_film_image_url(html)
    updated_fields = apply_scraped_fields(movieId, poster_url, synopsis, film_image_url)
    return {"movieId": movieId, "status": "success", "updatedFields": updated_fields}
