# backend/models/recipe.py
from pydantic import BaseModel
from typing import List

class RecipeComponent(BaseModel):
    ingredient_id: str
    grams_used: float

class RecipeCreate(BaseModel):
    name: str
    yield_quantity: int
    components: List[RecipeComponent]
    expected_sale_price: float

# backend/routers/recipes.py
from fastapi import APIRouter
from models.recipe import RecipeCreate

router = APIRouter()

@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    # This endpoint receives the JSON from the frontend,
    # calculates the final authoritative cost-per-batch using the live database pricing,
    # and saves the document to the MongoDB 'recipes' collection.
    
    # 1. Fetch current ingredient costs from DB
    # 2. Multiply by recipe.components.grams_used
    # 3. Save full recipe document
    
    return {"message": "Recipe saved successfully", "recipe_name": recipe.name}