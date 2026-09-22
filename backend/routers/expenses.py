from fastapi import APIRouter, HTTPException
from models.expense import Expense
from core.database import get_database
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

router = APIRouter()

@router.post("/")
async def log_expense(expense: Expense):
    db = get_database()
    doc = expense.model_dump()
    # Convert Pydantic date to full datetime for optimal MongoDB indexing
    doc["date"] = datetime.combine(doc["date"], datetime.min.time())
    
    result = await db.expenses.insert_one(doc)
    return {"message": "Expense logged", "id": str(result.inserted_id)}

@router.get("/")
async def get_expenses(skip: int = 0, limit: int = 100):
    db = get_database()
    expenses = await db.expenses.find().sort("date", -1).skip(skip).limit(limit).to_list(limit)
    for e in expenses:
        e["_id"] = str(e["_id"])
        # Format datetime back to string for the frontend
        if "date" in e and isinstance(e["date"], datetime):
            e["date"] = e["date"].strftime("%Y-%m-%d")
    return expenses

@router.delete("/{expense_id}")
async def delete_expense(expense_id: str):
    db = get_database()
    try:
        obj_id = ObjectId(expense_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Expense ID format")

    result = await db.expenses.delete_one({"_id": obj_id})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense not found")