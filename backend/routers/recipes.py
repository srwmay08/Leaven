# backend/routers/recipes.py
from fastapi import APIRouter, HTTPException
from models.recipe import RecipeCreate
from core.database import get_database

router = APIRouter()

@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    db = get_database()
    
    # Convert Pydantic model to a dict for MongoDB
    doc = {
        "name": recipe.name,
        "yield_qty": recipe.yield_qty,
        "ingredients": [{"name": i.name, "grams": i.grams} for i in recipe.ingredients]
    }
    
    result = await db.recipes.insert_one(doc)
    return {"message": "Saved successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_recipes():
    db = get_database()
    recipes = await db.recipes.find().to_list(1000)
    
    for recipe in recipes:
        recipe["_id"] = str(recipe["_id"])
        
    return recipes