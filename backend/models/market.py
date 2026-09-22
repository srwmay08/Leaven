from pydantic import BaseModel
from typing import List
from datetime import date

class MarketItem(BaseModel):
    item_key: str
    made_qty: int
    sold_qty: int

class MarketEvent(BaseModel):
    event_name: str
    event_date: date
    items: List[MarketItem]
    total_revenue: float
    total_cost: float
    total_profit: float