from typing import Iterator
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

agent = Agent(model=OpenAIChat(id="gpt-4o-mini"))

# # Run agent and return the response as a variable
# response: RunResponse = agent.run("Tell me a 5 second short story about a robot")
# # Run agent and return the response as a stream
# response_stream: Iterator[RunResponse] = agent.run("Tell me a 5 second short story about a lion", stream=True)

# # Print the response in markdown format
# # Print the response stream in markdown format
# pprint_run_response(response_stream, markdown=True)

response = agent.run("what is ai")

# print(response.content)
# pprint_run_response(response, markdown=True)

response_stream :Iterator[RunResponse] = agent.run("what is ai", stream=True)

for res in response_stream:
    print(res.content,flush=True,end="")
    