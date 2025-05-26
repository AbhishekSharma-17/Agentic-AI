from fastapi import APIRouter, HTTPException, Request, Depends
from composio_agno import ComposioToolSet, App
from database import db_manager, ComposioIntegration, AuthData, ConnectionMetadata
from datetime import datetime
import os
import uuid
from typing import Dict, Any, Optional
import asyncio

auth_router = APIRouter()

# Initialize Composio for Kroolo Agents
toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

class AuthService:
    def __init__(self):
        self.collection_name = "composio_integrations"
    
    async def get_collection(self):
        """Get the composio integrations collection"""
        return await db_manager.get_collection(self.collection_name)
    
    async def save_integration(self, integration_data: ComposioIntegration) -> str:
        """Save integration to MongoDB"""
        collection = await self.get_collection()
        
        # Convert to dict for MongoDB
        integration_dict = integration_data.dict()
        integration_dict["_id"] = str(uuid.uuid4())
        
        result = await collection.insert_one(integration_dict)
        return integration_dict["_id"]
    
    async def get_integration(self, user_id: str, organization_id: str, app_name: str) -> Optional[Dict]:
        """Get integration by user, org, and app"""
        collection = await self.get_collection()
        
        integration = await collection.find_one({
            "user_id": user_id,
            "organization_id": organization_id,
            "app_name": app_name,
            "is_deleted": False
        })
        
        return integration
    
    async def update_integration_status(self, integration_id: str, status: str, connection_data: Dict = None):
        """Update integration status and connection data"""
        collection = await self.get_collection()
        
        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }
        
        if connection_data:
            update_data.update(connection_data)
        
        await collection.update_one(
            {"_id": integration_id},
            {"$set": update_data}
        )
    
    async def delete_integration(self, user_id: str, organization_id: str, app_name: str):
        """Soft delete integration"""
        collection = await self.get_collection()
        
        await collection.update_one(
            {
                "user_id": user_id,
                "organization_id": organization_id,
                "app_name": app_name
            },
            {
                "$set": {
                    "is_deleted": True,
                    "updated_at": datetime.utcnow()
                }
            }
        )

auth_service = AuthService()

@auth_router.post("/connect")
async def initiate_connection(request: Request):
    """Initiate OAuth connection for any app - Kroolo Agents"""
    try:
        body = await request.json()
        user_id = body.get("user_id")
        organization_id = body.get("organization_id")
        app_name = body.get("app_name", "googlecalendar")
        
        if not user_id or not organization_id:
            raise HTTPException(status_code=400, detail="user_id and organization_id are required")
        
        # Check if integration already exists
        existing_integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if existing_integration and existing_integration.get("status") == "ACTIVE":
            return {
                "success": True,
                "message": "Already connected",
                "integration_id": existing_integration["_id"],
                "status": "ACTIVE"
            }
        
        # UPDATED: Use user_id directly as entity_id (not organization_id + user_id)
        entity_id = user_id
        entity = toolset.get_entity(id=entity_id)
        
        # Initiate connection
        connection_request = entity.initiate_connection(
            app_name=app_name,
            redirect_url=f"http://localhost:8000/auth/callback?user_id={user_id}&org_id={organization_id}&app_name={app_name}"
        )
        
        if connection_request.redirectUrl:
            # Save integration record
            integration_data = ComposioIntegration(
                user_id=user_id,
                organization_id=organization_id,
                app_name=app_name,
                connection_id=connection_request.connectedAccountId,
                status="PENDING",
                connection_metadata=ConnectionMetadata(
                    connected_at=datetime.utcnow(),
                    auth_method="OAUTH2",
                    redirect_uri=connection_request.redirectUrl
                )
            )
            
            integration_id = await auth_service.save_integration(integration_data)
            
            return {
                "success": True,
                "auth_url": connection_request.redirectUrl,
                "integration_id": integration_id,
                "user_id": user_id,
                "organization_id": organization_id,
                "app_name": app_name,
                "entity_id": entity_id  # Added for clarity
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to initiate OAuth flow")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/callback")
async def oauth_callback(user_id: str, org_id: str, app_name: str):
    """Handle OAuth callback - Kroolo Agents"""
    try:
        # Get the integration record
        integration = await auth_service.get_integration(user_id, org_id, app_name)
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Update status to ACTIVE
        await auth_service.update_integration_status(
            integration["_id"],
            "ACTIVE",
            {
                "connection_metadata.last_used": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        )
        
        return {
            "success": True,
            "message": f"Successfully connected {app_name} for Kroolo Agents",
            "user_id": user_id,
            "organization_id": org_id,
            "app_name": app_name,
            "status": "ACTIVE",
            "redirect_to": "http://localhost:8501"  # Streamlit app
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/status")
async def get_connection_status(user_id: str, organization_id: str, app_name: str):
    """Get connection status for a specific app - Kroolo Agents"""
    try:
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        
        if integration and integration.get("status") == "ACTIVE":
            return {
                "connected": True,
                "status": "ACTIVE",
                "app_name": app_name,
                "user_id": user_id,
                "organization_id": organization_id,
                "entity_id": user_id,  # Simplified entity ID
                "connected_at": integration.get("connection_metadata", {}).get("connected_at"),
                "last_used": integration.get("connection_metadata", {}).get("last_used")
            }
        else:
            return {
                "connected": False,
                "status": "NOT_CONNECTED",
                "app_name": app_name,
                "user_id": user_id,
                "organization_id": organization_id
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.delete("/disconnect")
async def disconnect_app(request: Request):
    """Disconnect an app integration - Kroolo Agents"""
    try:
        body = await request.json()
        user_id = body.get("user_id")
        organization_id = body.get("organization_id")
        app_name = body.get("app_name")
        
        if not all([user_id, organization_id, app_name]):
            raise HTTPException(status_code=400, detail="user_id, organization_id, and app_name are required")
        
        # Soft delete the integration
        await auth_service.delete_integration(user_id, organization_id, app_name)
        
        return {
            "success": True,
            "message": f"Successfully disconnected {app_name} from Kroolo Agents",
            "user_id": user_id,
            "organization_id": organization_id,
            "app_name": app_name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/integrations")
async def list_integrations(user_id: str, organization_id: str):
    """List all integrations for a user - Kroolo Agents"""
    try:
        collection = await auth_service.get_collection()
        
        integrations = await collection.find({
            "user_id": user_id,
            "organization_id": organization_id,
            "is_deleted": False
        }).to_list(length=None)
        
        return {
            "success": True,
            "integrations": integrations,
            "count": len(integrations),
            "user_id": user_id,
            "organization_id": organization_id,
            "entity_id": user_id  # Simplified entity ID
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
