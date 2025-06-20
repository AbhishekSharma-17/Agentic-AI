from agno.agent import Agent
from agno.models.openai import OpenAIChat
from rich.pretty import pprint

agent = Agent(
    model=OpenAIChat(id="gpt-4.1"),
    # Set add_history_to_messages=true to add the previous chat history to the messages sent to the Model.
    add_history_to_messages=True,
    # Number of historical responses to add to the messages.
    num_history_runs=3,
    debug_mode=True,
    description="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
)


while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    agent.print_response(user_input, stream=True)

