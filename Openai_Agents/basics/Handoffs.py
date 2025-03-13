from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak spanish"
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English"
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],   
)

async def main ():
    result = await Runner.run(starting_agent=orchestrator_agent, input="¿Cómo estás?")
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())