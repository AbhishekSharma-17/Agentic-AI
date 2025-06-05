import asyncio
from panda_agi import Agent
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    os.environ['PANDA_AGI_KEY'] = os.getenv('PANDAAGI_API_KEY')
    agent = Agent()
    
    async for event in agent.run_stream("its a productivity tool"):
        # Only print the text content of user_notification events
        if event.type == 'user_notification' and hasattr(event, 'text') and event.text:
            print(event.text)

asyncio.run(main())
