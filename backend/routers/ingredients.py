from fastapi import APIRouter, HTTPException
from models.ingredient import IngredientPurchase
from core.database import get_database

router = APIRouter()

@router.post("/")
async def create_ingredient(item: IngredientPurchase):
    db = get_database()
    
    # Calculate the exact cost per gram down to sub-cents
    if item.total_grams <= 0:
        raise HTTPException(status_code=400, detail="Total grams must be greater than zero.")
        
    cost_per_gram = item.purchase_price / item.total_grams
    
    # Construct the document for MongoDB
    doc = {
        "name": item.name,
        "purchase_price": item.purchase_price,
        "total_grams": item.total_grams,
        "cost_per_gram": cost_per_gram,
        "date": item.date.isoformat(),
        "vendor": item.vendor
    }
    
    # Insert the record into the 'ingredients' collection
    result = await db.ingredients.insert_one(doc)
    
    return {"message": "Saved successfully", "id": str(result.inserted_id)}

@router.get("/")
async def get_ingredients():
    db = get_database()
    
    # Fetch all inventory records to populate your frontend HTML table
    ingredients = await db.ingredients.find().to_list(1000)
    
    # Convert MongoDB's internal _id object to a string for the JSON response
    for ing in ingredients:
        ing["_id"] = str(ing["_id"])
        
    return ingredients