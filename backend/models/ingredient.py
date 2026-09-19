from pydantic import BaseModel
from datetime import date
from typing import Optional

# The Transaction (Wave/Zoho style)
class IngredientPurchase(BaseModel):
    date: date
    vendor: Optional[str] = None
    name: str
    purchase_price: float
    total_grams: float
    
    @property
    def cost_per_gram(self) -> float:
        return self.purchase_price / self.total_grams

# The Global Inventory State (Castiron style)
class GlobalIngredient(BaseModel):
    name: str
    current_stock_grams: float
    moving_average_cost_per_gram: float