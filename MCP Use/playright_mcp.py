import asyncio
import os
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

async def main():
    client = MCPClient(config=
    {
        "mcpServers": {
            "playwright": {
                "command": "npx",
                "args": ["@playwright/mcp@latest"],
                "env": { "DISPLAY": ":1" }
            }
        }
    }
    )
    # Create LLM
    llm = ChatOpenAI(model="gpt-4.1", api_key=openai_api_key)
    # Create agent with tools
    agent = MCPAgent(llm=llm, client=client, max_steps=30)
    # Run the query
    result = await agent.run("Find the best resturant in San Francisco")

if __name__ == "__main__":
    asyncio.run(main())