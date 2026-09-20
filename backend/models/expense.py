from pydantic import BaseModel

class Expense(BaseModel):
    date: str
    item_name: str
    category: str  # "Ingredient" or "Equipment"
    cost: float