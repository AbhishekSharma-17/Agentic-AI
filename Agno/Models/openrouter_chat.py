from agno.agent import Agent, RunResponse
from agno.models.openrouter import OpenRouter

agent = Agent(
    model=OpenRouter(id="gpt-4o"),
    markdown=True
)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story.")