from agno import agent
from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat

llm = OpenAIChat(id="gpt-4.1-mini")

agent = Agent(
    model=llm,
    markdown=True
)

agent.print_response("What is the capital of France?")
