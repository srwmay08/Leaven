from fastapi import APIRouter, HTTPException
from models.ingredient import Ingredient
from core.database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def create_ingredient(item: Ingredient):
    db = get_database()
    
    if item.total_grams <= 0:
        raise HTTPException(status_code=400, detail="Total grams must be greater than zero.")
        
    doc = {
        "name": item.name,
        "purchase_price": item.purchase_price,
        "total_grams": item.total_grams,
        "cost_per_gram": item.purchase_price / item.total_grams
    }
    
    result = await db.ingredients.insert_one(doc)
    return {"message": "Saved successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_ingredients():
    db = get_database()
    ingredients = await db.ingredients.find().sort("name", 1).to_list(1000)
    for ing in ingredients:
        ing["_id"] = str(ing["_id"])
    return ingredients

@router.put("/{item_id}")
async def update_ingredient(item_id: str, item: Ingredient):
    db = get_database()
    doc = {
        "name": item.name,
        "purchase_price": item.purchase_price,
        "total_grams": item.total_grams,
        "cost_per_gram": item.purchase_price / item.total_grams
    }
    result = await db.ingredients.update_one({"_id": ObjectId(item_id)}, {"$set": doc})
    if result.matched_count == 1:
        return {"message": "Updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
async def delete_ingredient(item_id: str):
    db = get_database()
    result = await db.ingredients.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")