from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.slack import SlackTools
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize SlackTools with your Slack token
slack_tools = SlackTools(
    token=os.getenv("SLACK_TOKENS"),  # Replace with your actual token
    send_message=True,                  # Enable sending messages
    list_channels=True,                 # Enable listing channels
    get_channel_history=True            # Enable getting channel history
)

# Create an agent with SlackTools
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[slack_tools],
    show_tool_calls=True,               # Show tool calls in the response
    markdown=True,                      # Format responses in markdown
    instructions=[
        "You are a helpful Slack assistant.",
        "You can send messages, list channels, and get channel history.",
        "Always confirm actions before executing them."
    ]
)

# Run the agent with a prompt
agent.print_response(
    "Send a message in new-channel , say Agno slack agent here sending this text on behalf of abhishek to check if it works, you have my permission post it ",
    stream=True
)