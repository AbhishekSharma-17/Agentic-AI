# Using Runner.run 

from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")

    result = await Runner.run(agent, "Write a haiku about recursion in programming.")
    print(result.final_output)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# using runner_sync 

agent = Agent(
    name="AI Abhi",
    instructions="You are an AI assistant designed to help users with their queries. Provide clear, concise, and helpful responses for a wide range of topics.",
)

result = Runner.run_sync(agent, "what is weather in jehanabd and cuurret day and date")

print(result.final_output)

