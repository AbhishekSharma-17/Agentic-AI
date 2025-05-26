# 🤖 Kroolo Agents

**Intelligent Automation Platform with AI-Powered Integrations**

Kroolo Agents is a powerful automation platform that combines AI-driven natural language processing with seamless app integrations via Composio. It enables users to manage their calendar, emails, and other productivity tools through intelligent agents that understand natural language commands.

## 🌟 Features

- **🤖 AI-Powered Calendar Agent**: Manage your calendar with natural language queries
- **📅 Smart Event Scheduling**: Schedule meetings with timezone awareness  
- **🔗 Seamless App Integrations**: Connect Google Calendar, Gmail, Slack, GitHub via Composio
- **🧠 Semantic Understanding**: Find events using semantic search (e.g., "composio meet" finds "Composio Integration" meeting)
- **🌍 Timezone Support**: Automatic timezone detection and handling
- **🎨 Beautiful UI**: Modern Streamlit interface with Kroolo branding
- **📊 Real-time Status**: Live connection status for all integrated apps

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐    OAuth2/Composio    ┌─────────────────┐
│                 │ ────────────►   │                 │ ─────────────────►   │                 │
│   Streamlit     │                 │   FastAPI       │                       │   Google        │
│   Frontend      │ ◄────────────   │   Backend       │ ◄─────────────────   │   Calendar      │
│   (Port 8501)   │                 │   (Port 8000)   │                       │   API           │
└─────────────────┘                 └─────────────────┘                       └─────────────────┘
        Kroolo Agents Interface               Kroolo Agents API
```

## 📁 Project Structure

```
kroolo-agents/
├── backend/
│   ├── main.py                 # FastAPI app - Kroolo Agents API
│   ├── auth.py                 # OAuth & authentication
│   ├── calendar_agent.py       # Composio calendar agent
│   ├── database.py             # MongoDB connection & models
│   └── requirements.txt
├── frontend/
│   ├── app.py                  # Main Streamlit app - Kroolo Agents UI
│   └── requirements.txt
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- Composio API key
- OpenAI API key

### 1. Environment Setup

Clone the repository and navigate to the project directory:

```bash
git clone <your-repo>
cd kroolo-agents
```

Set up your environment variables in `.env`:

```env
# Database
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority

# Composio
COMPOSIO_API_KEY=your_composio_api_key_here

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Streamlit
STREAMLIT_PORT=8501
```

### 2. Backend Setup

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal and install frontend dependencies:

```bash
cd frontend
pip install -r requirements.txt
```

Start the Streamlit app:

```bash
streamlit run app.py
```

The web interface will be available at `http://localhost:8501`

## 📖 Usage Guide

### 1. Setting Up User Context

1. Open the Kroolo Agents web interface at `http://localhost:8501`
2. In the sidebar, enter your:
   - **User ID**: Your Kroolo user identifier
   - **Organization ID**: Your Kroolo organization identifier
3. Click "🔄 Set Context" to save your settings

**Note**: The entity ID for Composio will be set to your User ID (simplified approach).

### 2. Connecting Apps

1. Navigate to the "🔗 Kroolo Agent Integrations" section
2. Click "🔗 Connect" for any app (Google Calendar, Gmail, etc.)
3. You'll receive an OAuth authorization URL
4. Click the link to authorize the app in a new tab
5. Return to the Kroolo Agents interface - the status will update to "✅ Connected"

### 3. Using the Calendar Agent

Once Google Calendar is connected, you can:

#### Natural Language Queries

- **"What meetings do I have today?"**
- **"Schedule a meeting with John tomorrow at 2 PM"**
- **"Find my composio meet"** (semantic search)
- **"Move my 3 PM meeting to 4 PM"**
- **"Cancel the standup meeting"**
- **"What's my next meeting?"**

#### Quick Actions

- **📋 Show Upcoming Events**: View your next 10 calendar events
- **🤖 Ask Kroolo Agent**: Type any calendar-related question

## 🔧 API Documentation

### Authentication Endpoints

#### `POST /auth/connect`
Initiate OAuth connection for any app.

```json
{
  "user_id": "your_user_id",
  "organization_id": "your_org_id", 
  "app_name": "googlecalendar"
}
```

#### `GET /auth/status`
Check connection status for a specific app.

Query parameters:
- `user_id`: User identifier
- `organization_id`: Organization identifier  
- `app_name`: App name (googlecalendar, gmail, etc.)

#### `DELETE /auth/disconnect`
Disconnect an app integration.

### Calendar Agent Endpoints

#### `POST /calendar/agent/query`
Query the AI calendar agent with natural language.

```json
{
  "user_id": "your_user_id",
  "organization_id": "your_org_id",
  "query": "What meetings do I have today?",
  "app_name": "googlecalendar"
}
```

#### `GET /calendar/events`
Get upcoming calendar events.

Query parameters:
- `user_id`: User identifier
- `organization_id`: Organization identifier
- `days_ahead`: Number of days to look ahead (default: 7)
- `app_name`: App name (default: googlecalendar)

## 🎯 Key Features

### Entity ID Simplification

Kroolo Agents uses a simplified entity ID approach:
- **Entity ID = User ID** (no more complex concatenation)
- This makes integration easier and more straightforward
- All Composio operations use the user_id directly as the entity_id

### Semantic Understanding

The AI agent can understand semantic meaning:
- **Query**: "composio meet"
- **Finds**: "Composio Integration" meeting
- **Query**: "team standup"  
- **Finds**: "Daily Standup" or "Team Standup Meeting"

### Timezone Awareness

- Automatic timezone detection using `tzlocal`
- All times displayed in user's local timezone
- Smart scheduling with timezone considerations

### Professional UI

- **Kroolo Branding**: Custom CSS with Kroolo color scheme
- **Status Indicators**: Clear connection status for each app
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live status updates and error handling

## 🛠️ Development

### Database Schema

The application uses MongoDB with the following collections:

#### `composio_integrations`
```json
{
  "_id": "unique_integration_id",
  "user_id": "user_identifier", 
  "organization_id": "org_identifier",
  "app_name": "googlecalendar",
  "connection_id": "composio_connection_id",
  "status": "ACTIVE",
  "connection_metadata": {
    "connected_at": "2024-01-01T00:00:00Z",
    "last_used": "2024-01-01T12:00:00Z",
    "auth_method": "OAUTH2"
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_deleted": false
}
```

### Adding New Apps

To add support for new apps:

1. **Add app configuration** in `frontend/app.py`:
   ```python
   {"name": "newapp", "title": "New App", "icon": "🔥"}
   ```

2. **Update calendar agent** in `backend/calendar_agent.py`:
   ```python
   apps=[App.NEWAPP] if app_name == "newapp" else [app_name]
   ```

3. **Test OAuth flow** with the new app

### Error Handling

The application includes comprehensive error handling:
- **Connection errors**: Graceful handling of network issues
- **OAuth failures**: Clear error messages for auth problems  
- **API errors**: Detailed error responses from backend
- **Database errors**: MongoDB connection error handling

## 📚 Dependencies

### Backend Dependencies
- **FastAPI**: Modern web framework for APIs
- **composio-agno**: Composio integration for agents
- **agno**: AI agent framework
- **motor**: Async MongoDB driver
- **uvicorn**: ASGI server
- **tzlocal**: Timezone detection

### Frontend Dependencies  
- **Streamlit**: Web app framework
- **requests**: HTTP client for API calls
- **tzlocal**: Timezone detection

## 🔒 Security

- **OAuth 2.0**: Secure app authorization flow
- **Environment Variables**: Sensitive data in .env files
- **Input Validation**: Request validation with Pydantic
- **CORS**: Proper CORS configuration for frontend/backend communication

## 🎉 Example Scenarios

### Scenario 1: Quick Meeting Check
**User**: "What's my next meeting?"
**Agent**: Analyzes calendar and responds with next upcoming meeting details including time, attendees, and location.

### Scenario 2: Smart Scheduling  
**User**: "Schedule a retrospective with the team for Friday at 3 PM"
**Agent**: Creates a new calendar event, invites team members, and confirms the meeting in user's timezone.

### Scenario 3: Semantic Search
**User**: "Find my composio meet"
**Agent**: Searches through calendar events, finds "Composio Integration Planning" meeting using semantic understanding.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the Kroolo team
- Check the API documentation at `http://localhost:8000/docs`

---

**Built with ❤️ by the Kroolo Team**
