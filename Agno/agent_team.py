from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools


web_agent = Agent(
    name="web_agent",
    role="search the web for information",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
     show_tool_calls=True,
     markdown=True
)

finance_agent = Agent(
    name="finance_agent",
    role="get finance data",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools(enable_all=True)],
    instructions="use tables to display data",
     show_tool_calls=True,
     markdown=True
)
agent_team = Agent(
    team=[web_agent, finance_agent],
    model=OpenAIChat(id="gpt-4o"),
    instructions=["Always include sources","use tables to display data"],
     show_tool_calls=True,
     markdown=True
)

agent_team.print_response("What's the market outlook and financial performance of AI semiconductor companies?", stream=True)
