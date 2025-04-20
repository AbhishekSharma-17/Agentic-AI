import os
from agno import agent
from agno.agent.agent import Agent
from agno.models.anthropic import Claude
from dotenv import load_dotenv

load_dotenv()

llm = Claude(api_key=os.getenv("ANTHROPIC_API_KEY"))

agent = Agent(
    model=llm,
    markdown=True
)

agent.print_response("Who are you?")
