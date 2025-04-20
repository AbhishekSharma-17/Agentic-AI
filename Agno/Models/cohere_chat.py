import os
from agno import agent
from agno.agent.agent import Agent
from agno.models.cohere import Cohere
from dotenv import load_dotenv

load_dotenv()

llm = Cohere(api_key=os.getenv("COHERE_API_KEY"))

agent = Agent(
    model=llm,
    markdown=True
)

agent.print_response("Who are you?")
