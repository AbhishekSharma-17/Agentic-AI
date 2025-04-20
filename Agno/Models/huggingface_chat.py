from agno.agent import Agent, RunResponse
from agno.models.huggingface import HuggingFace

agent = Agent(
    model=HuggingFace(
        id="meta-llama/Meta-Llama-3-8B-Instruct",
        max_tokens=4096,
    ),
    markdown=True
)

# Print the response on the terminal
agent.print_response("Share a 2 sentence horror story.")