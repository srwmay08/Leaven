# backend/routers/markets.py
from fastapi import APIRouter
from models.market import MarketEvent
from core.database import get_database

router = APIRouter()

@router.post("/")
async def log_market_event(event: MarketEvent):
    db = get_database()
    doc = event.model_dump()
    result = await db.markets.insert_one(doc)
    return {"message": "Event logged successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_market_events():
    db = get_database()
    events = await db.markets.find().to_list(1000)
    for e in events:
        e["_id"] = str(e["_id"])
    return events