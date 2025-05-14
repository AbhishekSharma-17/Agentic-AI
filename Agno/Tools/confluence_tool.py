from agno.agent import Agent
from agno.tools.confluence import ConfluenceTools

agent = Agent(
    name="Confluence agent",
    tools=[ConfluenceTools()],
    show_tool_calls=True,
    markdown=True,
)

agent.print_response("How many spaces are there and what are their names?")