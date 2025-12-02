from fastapi import APIRouter, Query
from ..services.batch_manager import start_batch
from ..config.settings import settings

router = APIRouter()

@router.post("/api/scrape/batch")
def start_scrape_batch(batch_size: int = Query(default=settings.BATCH_SIZE), rate_limit: float = Query(default=settings.WIKIPEDIA_RATE_LIMIT)):
    batch_id = start_batch(batch_size, rate_limit)
    return {"batchId": batch_id, "status": "running"}
