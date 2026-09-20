from fastapi import APIRouter, HTTPException
from models.recipe import RecipeCreate
from core.database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    db = get_database()
    
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

@router.put("/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: RecipeCreate):
    db = get_database()
    doc = {
        "name": recipe.name,
        "yield_qty": recipe.yield_qty,
        "ingredients": [{"name": i.name, "grams": i.grams} for i in recipe.ingredients]
    }
    result = await db.recipes.update_one({"_id": ObjectId(recipe_id)}, {"$set": doc})
    if result.matched_count == 1:
        return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str):
    db = get_database()
    result = await db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")