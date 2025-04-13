from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(model=OpenAIChat(api_key = os.getenv("OPENAI_API_KEY")),description="YOu are a unique joke writer who writes nice rhyming jokes",markdown=True)

agent.print_response("Tell me a joke about cats.",stream=True)