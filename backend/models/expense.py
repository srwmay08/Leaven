from pydantic import BaseModel
from datetime import date

class Expense(BaseModel):
    date: date
    item_name: str
    category: str  # "Ingredient" or "Equipment"
    cost: float