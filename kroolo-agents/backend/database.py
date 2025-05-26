from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel
import asyncio

# MongoDB connection
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://priyanshu:ZU0oUag2Tyu9jmNK@krooloprod.u99kr.mongodb.net/qastage01?retryWrites=true&w=majority")

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        self.client = AsyncIOMotorClient(DATABASE_URL)
        self.db = self.client.get_default_database()
        print("✅ Connected to MongoDB - Kroolo Agents")
        
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("❌ Disconnected from MongoDB - Kroolo Agents")
            
    async def get_collection(self, collection_name: str):
        """Get collection"""
        return self.db[collection_name]

# Global database manager
db_manager = DatabaseManager()

# Pydantic models for Kroolo Agents
class AuthData(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scopes: Optional[list] = []
    token_type: Optional[str] = "Bearer"

class ConnectionMetadata(BaseModel):
    connected_at: datetime
    last_used: Optional[datetime] = None
    auth_method: str = "OAUTH2"
    redirect_uri: Optional[str] = None
    user_email: Optional[str] = None

class ComposioIntegration(BaseModel):
    user_id: str
    organization_id: str
    app_name: str
    connection_id: Optional[str] = None
    integration_id: Optional[str] = None
    status: str = "PENDING"
    auth_data: Optional[AuthData] = None
    connection_metadata: Optional[ConnectionMetadata] = None
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    is_deleted: bool = False
