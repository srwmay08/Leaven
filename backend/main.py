from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles

from core.database import connect_to_mongo, close_mongo_connection
from routers import ingredients, recipes, markets, receipts, expenses

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="MaykeryOS API",
    lifespan=lifespan
)

# Using a wildcard allows local network access (e.g., from a tablet on your Wi-Fi).
# If deploying to production, replace "*" with your specific production domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingredients.router, prefix="/api/ingredients", tags=["Ingredients"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recipes"])
app.include_router(markets.router, prefix="/api/markets", tags=["Markets"])
app.include_router(receipts.router, prefix="/api/receipts", tags=["Receipts"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")