import os
from agents import Agent , Runner

agent = Agent(name="My AI",
              instructions="you are an helpfull assistant",
              model="gpt-4o"
              )

result = Runner.run_sync(agent, "what is ai")

print(result.final_output)