import os
from agno import agent
from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

llm = OpenAIChat(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    id="deepseek/deepseek-chat-v3-0324",  # Using a likely available model
    
)

agent = Agent(
    model=llm,
    markdown=True
)

agent.print_response("Who are you?")
