from agno.agent import Agent, RunResponse
from agno.models.nvidia import Nvidia

agent = Agent(model=Nvidia(), markdown=True)

# Print the response in the terminal
agent.print_response("Share a 2 sentence horror story")