from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles # 1. Import StaticFiles

from core.database import connect_to_mongo, close_mongo_connection
from routers import ingredients, recipes, markets

# backend/routers/recipes.py
from fastapi import APIRouter
router = APIRouter()

# backend/routers/markets.py
from fastapi import APIRouter
router = APIRouter()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="MaykeryOS API",
    lifespan=lifespan
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Register API routers FIRST
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["Ingredients"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recipes"])
app.include_router(markets.router, prefix="/api/markets", tags=["Markets"])

# 3. Mount the frontend directory LAST
# The path "../frontend" assumes your terminal is running from inside the /backend directory.
# html=True tells FastAPI to automatically serve index.html when you visit the root URL.
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")