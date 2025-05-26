import os
from agno.agent import Agent
from composio_agno.toolset import Action, ComposioToolSet
from dotenv import load_dotenv

load_dotenv()

toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"),
                          allow_tracing=True
                          )
composio_tools = toolset.get_tools(
  actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
)

agent = Agent(tools=composio_tools, show_tool_calls=True)
agent.print_response("Can you star agno-agi/agno repo?")