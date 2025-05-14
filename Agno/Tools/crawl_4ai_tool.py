from agno.agent import Agent
from agno.tools.crawl4ai import Crawl4aiTools

agent = Agent(tools=[Crawl4aiTools(max_length=None)], show_tool_calls=True)
response = agent.run("Tell me about https://kroolo.com/")
print(response.content)