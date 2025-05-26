from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import db_manager
import os
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    await db_manager.connect()
    print("🚀 Kroolo Agents API - Connected to MongoDB")
    
    yield
    
    # Shutdown
    await db_manager.disconnect()
    print("🛑 Kroolo Agents API - Disconnected from MongoDB")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="Kroolo Agents API",
    description="Intelligent Automation Platform with AI-Powered Integrations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Kroolo Agents API",
        "status": "active",
        "version": "1.0.0",
        "description": "Intelligent Automation Platform with AI-Powered Integrations"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "platform": "Kroolo Agents",
        "database": "connected"
    }

# Include routers
from auth import auth_router
from calendar_agent import calendar_router

app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
