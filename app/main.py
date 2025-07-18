# Environment variables are loaded from .env and used in database.py for MongoDB connection
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import client
from app.routers.recipes import router as recipes_router
from app.routers.admin import router as admin_router
from app.routers.generation import router as generation_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(recipes_router)
app.include_router(admin_router)
app.include_router(generation_router)


