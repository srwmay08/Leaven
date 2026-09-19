# backend/models/market.py
from pydantic import BaseModel
from typing import List

class MarketItem(BaseModel):
    item_key: str
    made_qty: int
    sold_qty: int

class MarketEvent(BaseModel):
    event_name: str
    event_date: str
    items: List[MarketItem]
    total_revenue: float
    total_cost: float
    total_profit: float