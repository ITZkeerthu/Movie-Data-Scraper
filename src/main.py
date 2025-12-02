from fastapi import FastAPI
import logging
from .config import settings
from .api.scrape import router as scrape_router
from .api.movies import router as movies_router

app = FastAPI(title="Movie Data Scraper")
logger = logging.getLogger("uvicorn.error")

@app.get("/")
async def root():
    return {"status": "ok", "feature": "movie-data-scraper"}

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Movie Data Scraper service")

app.include_router(scrape_router)
app.include_router(movies_router)
