import asyncio
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools


async def run_agent(message: str) -> None:
    """Run the Airbnb and Google Maps agent with the given message."""
    
    user_id = "keshavgarg"
    linkedin = "default"
    gmail_mcp = f"https://mcp.composio.dev/composio/server/bd8ab3d4-8959-48f6-82c9-dcf364435ab8/mcp?user_id={user_id}"
    linkedin_mcp = f"https://mcp.composio.dev/composio/server/b1da7b3d-2314-4cbd-9af7-bf4ac710468f/mcp?user_id={linkedin}"
    
    async with MultiMCPTools(
        urls=[
            gmail_mcp,
            linkedin_mcp
        ],
        urls_transports=["streamable-http","streamable-http"]
    ) as mcp_tools:
        agent = Agent(
            tools=[mcp_tools],
            markdown=True,
            show_tool_calls=True,
        )

        await agent.aprint_response(message, stream=True)


# Example usage
if __name__ == "__main__":
    while True:
        message = input("You: ")
        asyncio.run(
            run_agent(
                message=message
            )
        )
