from fastapi import APIRouter, HTTPException
from models.expense import Expense
from core.database import get_database
from bson import ObjectId

router = APIRouter()

@router.post("/")
async def log_expense(expense: Expense):
    db = get_database()
    doc = expense.model_dump()
    result = await db.expenses.insert_one(doc)
    return {"message": "Expense logged", "id": str(result.inserted_id)}

@router.get("/")
async def get_expenses():
    db = get_database()
    expenses = await db.expenses.find().sort("date", -1).to_list(1000)
    for e in expenses:
        e["_id"] = str(e["_id"])
    return expenses

@router.delete("/{expense_id}")
async def delete_expense(expense_id: str):
    db = get_database()
    result = await db.expenses.delete_one({"_id": ObjectId(expense_id)})
    if result.deleted_count == 1:
        return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Expense not found")