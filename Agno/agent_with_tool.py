from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

import os
from dotenv import load_dotenv

load_dotenv()

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY")),
    description="you are a research agent",
    show_tool_calls=True,
    tools=[DuckDuckGoTools()],
    markdown=True
)
agent.print_response("What's the recent ipl match results", stream=True)