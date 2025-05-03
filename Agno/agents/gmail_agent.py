from agno.agent import Agent
from pathlib import Path
from dotenv import load_dotenv

from custom_gmail_tools import FixedPortGmailTools

# Load environment variables from .env file
dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

# Create token path in the same directory
token_path = str(Path(__file__).parent / "gmail_token.json")

# Define explicit scopes
scopes = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.compose",
]

# Initialize our custom FixedPortGmailTools with explicit parameters
agent = Agent(
    tools=[
        FixedPortGmailTools(
            port=8000,  # Explicitly set the port to match client_secret.json
            credentials_path="client_secret.json",
            token_path=token_path,
            scopes=scopes
        )
    ],
    show_tool_calls=True
)

agent.print_response("send a mail to keshav.garg@genaiprotos.com , Hey there Agno bot here have a safe trip just letting you know abhishek has completed the oauth for me and now im working", markdown=True)
