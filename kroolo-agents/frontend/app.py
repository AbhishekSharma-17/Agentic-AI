import streamlit as st
import requests
import json
from datetime import datetime
from tzlocal import get_localzone_name
from dotenv import load_dotenv
import os

load_dotenv()

# Page config
st.set_page_config(
    page_title="Kroolo Agents",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for modern professional Kroolo branding
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #FAFBFC;
    }
    
    /* Modern Professional Header */
    .kroolo-header {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 50%, #2980B9 100%);
        padding: 2rem 1rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(52, 73, 94, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .kroolo-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .kroolo-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Modern Card Design */
    .kroolo-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3498DB;
        margin: 1.5rem 0;
        box-shadow: 0 4px 16px rgba(52, 73, 94, 0.08);
        border: 1px solid #E5E8EB;
        transition: all 0.3s ease;
    }
    
    .kroolo-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(52, 73, 94, 0.12);
    }
    
    .kroolo-card h3, .kroolo-card h4 {
        color: #2C3E50 !important;
        font-weight: 600;
    }
    
    .kroolo-card p, .kroolo-card li {
        color: #34495E !important;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Status Indicators */
    .status-connected {
        background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(39, 174, 96, 0.3);
        border: none;
    }
    
    .status-disconnected {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
        border: none;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background-color: #F8F9FA;
        border-right: 2px solid #E5E8EB;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980B9 0%, #1F4E79 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
    }
    
    /* Text Input Styling */
    .stTextInput > div > div > input {
        border: 2px solid #E5E8EB;
        border-radius: 8px;
        padding: 0.75rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3498DB;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #D5F4E6 0%, #FAFFFE 100%);
        border-left: 4px solid #27AE60;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #FADBD8 0%, #FAFFFE 100%);
        border-left: 4px solid #E74C3C;
        border-radius: 8px;
    }
    
    /* Agent Response Styling */
    .agent-response {
        background: linear-gradient(145deg, #EBF3FD 0%, #F8FBFF 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #5DADE2;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(93, 173, 226, 0.1);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #E5E8EB;
        text-align: center;
        box-shadow: 0 2px 8px rgba(52, 73, 94, 0.05);
    }
    
    .metric-card h4 {
        color: #2C3E50 !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #34495E !important;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Professional Typography */
    h1, h2, h3, h4 {
        color: #2C3E50;
        font-weight: 600;
    }
    
    .sidebar-metric {
        background: linear-gradient(135deg, #85C1AE 0%, #A8E6CF 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 6px;
        text-align: center;
        font-weight: 500;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Backend API base URL
API_BASE = "http://localhost:8000"

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "organization_id" not in st.session_state:
    st.session_state.organization_id = None
if "integrations" not in st.session_state:
    st.session_state.integrations = {}

def main():
    # Kroolo Agents Header
    st.markdown("""
    <div class="kroolo-header">
        <h1>🤖 Kroolo Agents</h1>
        <p>Intelligent Automation Platform with AI-Powered Integrations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Context Input
    st.sidebar.header("🔐 User Context")
    st.sidebar.markdown("**Kroolo Agents Configuration**")
    
    user_id = st.sidebar.text_input(
        "User ID", 
        value=st.session_state.user_id or "",
        placeholder="Enter your Kroolo user ID"
    )
    
    organization_id = st.sidebar.text_input(
        "Organization ID",
        value=st.session_state.organization_id or "",
        placeholder="Enter your Kroolo organization ID"
    )
    
    if st.sidebar.button("🔄 Set Context"):
        if user_id and organization_id:
            st.session_state.user_id = user_id
            st.session_state.organization_id = organization_id
            st.success(f"✅ Kroolo Agent context set for User: {user_id}, Org: {organization_id}")
            st.rerun()
        else:
            st.error("Both User ID and Organization ID are required")
    
    # Show current context
    if st.session_state.user_id and st.session_state.organization_id:
        st.sidebar.success(f"✅ User: {st.session_state.user_id}")
        st.sidebar.success(f"✅ Org: {st.session_state.organization_id}")
        st.sidebar.info(f"🌍 Timezone: {get_localzone_name()}")
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Entity ID (Composio):** " + st.session_state.user_id)
        
        # Main app content
        show_main_interface()
    else:
        st.markdown("""
        <div class="kroolo-card">
            <h3>👋 Welcome to Kroolo Agents</h3>
            <p>Please set your User ID and Organization ID in the sidebar to start using your intelligent agents.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>🤖 AI-powered calendar management</li>
                <li>📅 Smart event scheduling with timezone awareness</li>
                <li>🔗 Seamless app integrations via Composio</li>
                <li>🧠 Semantic understanding of natural language queries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_main_interface():
    """Main interface when user context is set - Kroolo Agents"""
    
    # Apps Integration Section
    st.header("🔗 Kroolo Agent Integrations")
    st.markdown("Connect your favorite apps to enable intelligent automation")
    
    apps = [
        {"name": "googlecalendar", "title": "Google Calendar", "icon": "📅"},
        {"name": "gmail", "title": "Gmail", "icon": "📧"},
        {"name": "slack", "title": "Slack", "icon": "💬"},
        {"name": "github", "title": "GitHub", "icon": "🐙"}
    ]
    
    cols = st.columns(len(apps))
    
    for idx, app in enumerate(apps):
        with cols[idx]:
            st.markdown(f"""
            <div class="kroolo-card">
                <h4>{app['icon']} {app['title']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Check connection status
            try:
                status_response = requests.get(
                    f"{API_BASE}/auth/status",
                    params={
                        "user_id": st.session_state.user_id,
                        "organization_id": st.session_state.organization_id,
                        "app_name": app['name']
                    }
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    is_connected = status_data.get("connected", False)
                    
                    if is_connected:
                        st.markdown('<div class="status-connected">✅ Connected</div>', unsafe_allow_html=True)
                        if st.button(f"🔓 Disconnect", key=f"disconnect_{app['name']}"):
                            disconnect_app(app['name'])
                    else:
                        st.markdown('<div class="status-disconnected">❌ Not Connected</div>', unsafe_allow_html=True)
                        if st.button(f"🔗 Connect", key=f"connect_{app['name']}"):
                            connect_app(app['name'])
                else:
                    st.error("Error checking status")
            except Exception as e:
                st.error(f"Connection error: {e}")
    
    st.markdown("---")
    
    # Calendar Agent Interface (only show if Google Calendar is connected)
    try:
        gcal_status = requests.get(
            f"{API_BASE}/auth/status",
            params={
                "user_id": st.session_state.user_id,
                "organization_id": st.session_state.organization_id,
                "app_name": "googlecalendar"
            }
        )
        
        if gcal_status.status_code == 200 and gcal_status.json().get("connected"):
            show_calendar_agent()
        else:
            st.markdown("""
            <div class="kroolo-card">
                <h3>📅 Calendar Agent</h3>
                <p>Connect Google Calendar to enable your AI-powered calendar assistant.</p>
                <p>Once connected, you'll be able to:</p>
                <ul>
                    <li>Schedule meetings with natural language</li>
                    <li>Find events using semantic search</li>
                    <li>Manage your calendar with timezone awareness</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error checking calendar status: {e}")

def connect_app(app_name: str):
    """Connect an app via OAuth"""
    try:
        with st.spinner(f"Initiating {app_name} connection..."):
            response = requests.post(
                f"{API_BASE}/auth/connect",
                json={
                    "user_id": st.session_state.user_id,
                    "organization_id": st.session_state.organization_id,
                    "app_name": app_name
                }
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                auth_url = result.get("auth_url")
                if auth_url:
                    st.success(f"✅ OAuth initiated for {app_name}")
                    st.markdown(f"**[Click here to authorize {app_name}]({auth_url})**")
                else:
                    st.info(f"Already connected to {app_name}")
            else:
                st.error("Failed to initiate OAuth")
        else:
            st.error(f"Error: {response.text}")
            
    except Exception as e:
        st.error(f"Connection error: {e}")

def disconnect_app(app_name: str):
    """Disconnect an app"""
    try:
        with st.spinner(f"Disconnecting {app_name}..."):
            response = requests.delete(
                f"{API_BASE}/auth/disconnect",
                json={
                    "user_id": st.session_state.user_id,
                    "organization_id": st.session_state.organization_id,
                    "app_name": app_name
                }
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                st.success(f"✅ Disconnected from {app_name}")
                st.rerun()
            else:
                st.error("Failed to disconnect")
        else:
            st.error(f"Error: {response.text}")
            
    except Exception as e:
        st.error(f"Disconnection error: {e}")

def show_calendar_agent():
    """Kroolo Calendar Agent interface"""
    st.header("🤖 Kroolo Calendar Agent")
    st.markdown(f"**Timezone:** {get_localzone_name()} | **Current time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Entity ID:** {st.session_state.user_id}")
    
    # Example queries
    with st.expander("💡 Example Queries for your Kroolo Agent"):
        st.markdown("""
        - "Schedule a meeting with John tomorrow at 2 PM"
        - "What meetings do I have today?"
        - "Find my composio meet" (will find "Composio Integration" meeting)
        - "Move my 3 PM meeting to 4 PM"
        - "Cancel the standup meeting"
        - "What's my next meeting?"
        - "Schedule a team retrospective for Friday at 3 PM"
        """)
    
    # Query input
    user_query = st.text_area(
        "Ask your Kroolo Calendar Agent:",
        placeholder="e.g., 'What meetings do I have today?' or 'Schedule a team standup for tomorrow at 10 AM'",
        height=100
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🤖 Ask Kroolo Agent", disabled=not user_query.strip()):
            if user_query.strip():
                query_calendar_agent(user_query.strip())
    
    with col2:
        if st.button("📋 Show Upcoming Events"):
            show_upcoming_events()

def query_calendar_agent(query: str):
    """Query the Kroolo calendar agent"""
    try:
        with st.spinner("🤖 Your Kroolo Agent is processing..."):
            response = requests.post(
                f"{API_BASE}/calendar/agent/query",
                json={
                    "user_id": st.session_state.user_id,
                    "organization_id": st.session_state.organization_id,
                    "query": query,
                    "app_name": "googlecalendar"
                }
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                st.markdown("### 🤖 Kroolo Agent Response:")
                st.markdown(f"""
                <div class="agent-response">
                    {result.get("response")}
                </div>
                """, unsafe_allow_html=True)
                
                # Show metadata in a professional card
                with st.expander("📊 Response Analytics", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>🏢 Platform</h4>
                            <p>{result.get("agent_platform", "N/A")}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>🌍 Timezone</h4>
                            <p>{result.get("timezone", "N/A")}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>🆔 Entity ID</h4>
                            <p>{result.get("entity_id", "N/A")}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.json({
                        "timestamp": result.get("timestamp"),
                        "user_id": result.get("user_id"),
                        "organization_id": result.get("organization_id")
                    })
            else:
                st.error("❌ Failed to get response from Kroolo Agent")
        else:
            st.error(f"❌ Error: {response.text}")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

def show_upcoming_events():
    """Show upcoming calendar events"""
    try:
        with st.spinner("📅 Fetching your events..."):
            response = requests.get(
                f"{API_BASE}/calendar/events",
                params={
                    "user_id": st.session_state.user_id,
                    "organization_id": st.session_state.organization_id,
                    "days_ahead": 7,
                    "app_name": "googlecalendar"
                }
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                events = result.get("events", [])
                if events:
                    st.success(f"📅 Found {len(events)} upcoming events:")
                    for event in events:
                        with st.expander(f"📅 {event.get('summary', 'No Title')}"):
                            st.write(f"**Start:** {event.get('start', {}).get('dateTime', 'TBD')}")
                            st.write(f"**End:** {event.get('end', {}).get('dateTime', 'TBD')}")
                            if event.get('description'):
                                st.write(f"**Description:** {event.get('description')}")
                            if event.get('attendees'):
                                st.write(f"**Attendees:** {len(event.get('attendees'))} people")
                else:
                    st.info("📅 No upcoming events found")
            else:
                st.error("❌ Failed to fetch events")
        else:
            st.error(f"❌ Error: {response.text}")
            
    except Exception as e:
        st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
