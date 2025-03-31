from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(model=OpenAIChat(),description="YOu are a unique joke writer who writes nice rhyming jokes",markdown=True)

agent.print_response("Tell me a joke about cats.",stream=True)