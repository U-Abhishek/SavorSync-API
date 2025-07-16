# Environment variables are loaded from .env and used in database.py for MongoDB connection
from fastapi import FastAPI, HTTPException
from app.database import client
from app.routers.recipes import router as recipes_router
from app.routers.admin import router as admin_router

app = FastAPI()

app.include_router(recipes_router)
app.include_router(admin_router)


