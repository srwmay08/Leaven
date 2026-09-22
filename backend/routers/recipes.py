from fastapi import APIRouter, HTTPException
from models.recipe import RecipeCreate  # Assumes RecipeCreate model exists
from core.database import get_database
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.post("/")
async def create_recipe(recipe: RecipeCreate):
    db = get_database()
    doc = recipe.model_dump()
    result = await db.recipes.insert_one(doc)
    return {"message": "Saved successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_recipes(skip: int = 0, limit: int = 100):
    db = get_database()
    recipes = await db.recipes.find().skip(skip).limit(limit).to_list(limit)
    for recipe in recipes:
        recipe["_id"] = str(recipe["_id"])
    return recipes

@router.put("/{recipe_id}")
async def update_recipe(recipe_id: str, recipe: RecipeCreate):
    db = get_database()
    try:
        obj_id = ObjectId(recipe_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Recipe ID format")

    doc = recipe.model_dump()
    result = await db.recipes.update_one({"_id": obj_id}, {"$set": doc})
    if result.matched_count == 1:
        return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str):
    db = get_database()
    try:
        obj_id = ObjectId(recipe_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Recipe ID format")

    result = await db.recipes.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")