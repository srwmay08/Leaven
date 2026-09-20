from pydantic import BaseModel
from typing import List

class RecipeIngredient(BaseModel):
    name: str
    grams: float

class RecipeCreate(BaseModel):
    name: str
    yield_qty: int
    ingredients: List[RecipeIngredient]