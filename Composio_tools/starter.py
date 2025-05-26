from agno.agent.agent import Agent
from composio_agno import Action, App, ComposioToolSet
import os
from dotenv import load_dotenv

load_dotenv()


toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

# request = toolset.initiate_connection(app=App.GITHUB)
# print(f"Open this URL to authenticate: {request.redirectUrl}")

# You can get all the tools for a given app
tools = toolset.get_tools(apps=[App.GITHUB])


agent = Agent(tools=tools, show_tool_calls=True)

agent.print_response("Can you star ComposioHQ/composio repo?")
