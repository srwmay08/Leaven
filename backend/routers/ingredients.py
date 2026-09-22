from fastapi import APIRouter, HTTPException
from models.ingredient import Ingredient
from core.database import get_database
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter()

@router.post("/")
async def create_ingredient(item: Ingredient):
    db = get_database()
    doc = item.model_dump()
    result = await db.ingredients.insert_one(doc)
    return {"message": "Saved successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_ingredients(skip: int = 0, limit: int = 100):
    db = get_database()
    ingredients = await db.ingredients.find().sort("name", 1).skip(skip).limit(limit).to_list(limit)
    for ing in ingredients:
        ing["_id"] = str(ing["_id"])
    return ingredients

@router.put("/{item_id}")
async def update_ingredient(item_id: str, item: Ingredient):
    db = get_database()
    try:
        obj_id = ObjectId(item_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Ingredient ID format")

    doc = item.model_dump()
    result = await db.ingredients.update_one({"_id": obj_id}, {"$set": doc})
    if result.matched_count == 1:
        return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
async def delete_ingredient(item_id: str):
    db = get_database()
    try:
        obj_id = ObjectId(item_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Ingredient ID format")

    result = await db.ingredients.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")