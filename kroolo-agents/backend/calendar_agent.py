from fastapi import APIRouter, HTTPException
from composio_agno import ComposioToolSet, App, Action
from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from database import db_manager
from auth import auth_service
from tzlocal import get_localzone_name
import datetime
import os

calendar_router = APIRouter()

toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

@calendar_router.post("/agent/query")
async def query_calendar_agent(data: dict):
    """Kroolo Agents - Enhanced calendar agent with timezone and semantic understanding"""
    try:
        user_id = data.get("user_id")
        organization_id = data.get("organization_id")
        query = data.get("query")
        app_name = data.get("app_name", "googlecalendar")
        
        if not all([user_id, organization_id, query]):
            raise HTTPException(
                status_code=400, 
                detail="user_id, organization_id, and query are required"
            )
        
        # Check if user has active connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found. Please connect first."
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Get tools for the specific app
        tools = toolset.get_tools(
            apps=[App.GOOGLECALENDAR] if app_name == "googlecalendar" else [app_name]
        )
        
        # Enhanced Kroolo Agent with timezone and semantic understanding
        agent = Agent(
            model=OpenAIChat(api_key=os.getenv("OPENAI_API_KEY")),
            tools=tools,
            description="Kroolo Agents - Smart calendar assistant with timezone awareness and semantic understanding",
            show_tool_calls=True,
            add_datetime_to_instructions=True,
            instructions=[
                f"Today is {datetime.datetime.now()} and the user's timezone is {get_localzone_name()}",
                "You are part of Kroolo Agents - an intelligent automation platform",
                "List all the meetings and analyze the query to target correct meetings or events",
                "For example, if the meeting title is 'Composio Integration' but user says 'composio meet', understand the semantic meaning and choose the correct meeting",
                "Use semantic understanding to match user queries with calendar events even if exact words don't match",
                "Always consider the user's timezone when scheduling or discussing times",
                "Be helpful and provide clear responses about calendar operations",
                "If creating events, always confirm the time zone and ask for clarification if needed",
                "When listing events, show them in the user's local timezone",
                "Always maintain a professional and helpful tone as a Kroolo Agent"
            ]
        )
        
        # Use agent.run() to get RunResponse object
        run_response = agent.run(query)
        
        # Update last used timestamp
        await auth_service.update_integration_status(
            integration["_id"],
            "ACTIVE",
            {"connection_metadata.last_used": datetime.datetime.utcnow()}
        )
        
        # Extract serializable content from RunResponse
        response_content = str(run_response.content) if run_response.content else "No response"
        
        # Convert messages to serializable format
        messages_data = []
        if hasattr(run_response, 'messages') and run_response.messages:
            for msg in run_response.messages:
                messages_data.append({
                    "role": getattr(msg, 'role', 'unknown'),
                    "content": str(getattr(msg, 'content', ''))
                })
        
        return {
            "success": True,
            "response": response_content,
            "messages": messages_data,
            "user_id": user_id,
            "organization_id": organization_id,
            "entity_id": entity_id,
            "app_name": app_name,
            "timezone": get_localzone_name(),
            "timestamp": datetime.datetime.now().isoformat(),
            "agent_platform": "Kroolo Agents"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.get("/events")
async def get_calendar_events(
    user_id: str, 
    organization_id: str, 
    days_ahead: int = 7,
    app_name: str = "googlecalendar"
):
    """Kroolo Agents - Get upcoming calendar events with timezone support"""
    try:
        # Check connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found"
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Execute calendar action
        list_event_tool = toolset.get_tools(actions=[Action.GOOGLECALENDAR_LIST_CALENDARS])
        
        
        
        if result.get("successful"):
            return {
                "success": True,
                "events": result.get("data", []),
                "timezone": get_localzone_name(),
                "fetched_at": datetime.datetime.now().isoformat(),
                "entity_id": entity_id,
                "agent_platform": "Kroolo Agents"
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.post("/events")
async def create_calendar_event(data: dict):
    """Kroolo Agents - Create a new calendar event"""
    try:
        user_id = data.get("user_id")
        organization_id = data.get("organization_id")
        event_data = data.get("event_data")
        app_name = data.get("app_name", "googlecalendar")
        
        if not all([user_id, organization_id, event_data]):
            raise HTTPException(
                status_code=400, 
                detail="user_id, organization_id, and event_data are required"
            )
        
        # Check connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found"
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Execute create event action
        result = toolset.execute_action(
            action="GOOGLECALENDAR_LIST_CALENDARS",
            params=event_data,
            entity_id=entity_id
        )
        
        if result.get("successful"):
            return {
                "success": True,
                "event": result.get("data"),
                "message": "Event created successfully by Kroolo Agents",
                "entity_id": entity_id,
                "agent_platform": "Kroolo Agents"
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.put("/events/{event_id}")
async def update_calendar_event(event_id: str, data: dict):
    """Kroolo Agents - Update an existing calendar event"""
    try:
        user_id = data.get("user_id")
        organization_id = data.get("organization_id")
        event_updates = data.get("event_updates")
        app_name = data.get("app_name", "googlecalendar")
        
        if not all([user_id, organization_id, event_updates]):
            raise HTTPException(
                status_code=400, 
                detail="user_id, organization_id, and event_updates are required"
            )
        
        # Check connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found"
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Add event ID to the update parameters
        update_params = {**event_updates, "eventId": event_id}
        
        # Execute update event action
        result = toolset.execute_action(
            action="GOOGLECALENDAR_UPDATE_EVENT",
            params=update_params,
            entity_id=entity_id
        )
        
        if result.get("successful"):
            return {
                "success": True,
                "event": result.get("data"),
                "message": "Event updated successfully by Kroolo Agents",
                "entity_id": entity_id,
                "agent_platform": "Kroolo Agents"
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.delete("/events/{event_id}")
async def delete_calendar_event(event_id: str, user_id: str, organization_id: str, app_name: str = "googlecalendar"):
    """Kroolo Agents - Delete a calendar event"""
    try:
        # Check connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found"
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Execute delete event action
        result = toolset.execute_action(
            action="GOOGLECALENDAR_DELETE_EVENT",
            params={"eventId": event_id},
            entity_id=entity_id
        )
        
        if result.get("successful"):
            return {
                "success": True,
                "message": "Event deleted successfully by Kroolo Agents",
                "event_id": event_id,
                "entity_id": entity_id,
                "agent_platform": "Kroolo Agents"
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@calendar_router.get("/calendars")
async def list_calendars(user_id: str, organization_id: str, app_name: str = "googlecalendar"):
    """Kroolo Agents - List all available calendars"""
    try:
        # Check connection
        integration = await auth_service.get_integration(user_id, organization_id, app_name)
        if not integration or integration.get("status") != "ACTIVE":
            raise HTTPException(
                status_code=401,
                detail=f"No active {app_name} connection found"
            )
        
        # UPDATED: Use user_id directly as entity_id
        entity_id = user_id
        
        # Execute list calendars action
        result = toolset.execute_action(
            action="GOOGLECALENDAR_LIST_CALENDARS",
            params={},
            entity_id=entity_id
        )
        
        if result.get("successful"):
            return {
                "success": True,
                "calendars": result.get("data", []),
                "entity_id": entity_id,
                "agent_platform": "Kroolo Agents"
            }
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
