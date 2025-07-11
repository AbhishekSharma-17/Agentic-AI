import asyncio
from agno.agent import Agent
from agno.tools.mcp import MultiMCPTools

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools

user_id = "keshavgarg"

gmail_mcp = f"https://mcp.composio.dev/composio/server/bd8ab3d4-8959-48f6-82c9-dcf364435ab8/mcp?user_id={user_id}"
async def run_agent(message: str) -> None:
    """Acces to figma ."""

    async with MCPTools(url=gmail_mcp, transport="streamable-http") as mcp_tools:
        agent = Agent(model=OpenAIChat(id="gpt-4.1"), tools=[mcp_tools],add_history_to_messages=True,num_history_runs=3)
        await agent.aprint_response(message=message, stream=True)


# Example usage
if __name__ == "__main__":
    # Pull request example
    while True:
        message = input("You: ")
        asyncio.run(
            run_agent(
                message=message
            )
        )