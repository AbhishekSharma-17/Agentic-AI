"""
🔒 Using Pipedream MCP servers with authentication

This is an example of how to use Pipedream MCP servers with authentication.
This is useful if your app is interfacing with the MCP servers in behalf of your users.

1. Get your access token. You can check how in Pipedream's docs: https://pipedream.com/docs/connect/mcp/developers/
2. Get the URL of the MCP server. It will look like this: https://remote.mcp.pipedream.net/<External user id>/<MCP app slug>
3. Set the environment variables:
    - MCP_SERVER_URL: The URL of the MCP server you previously got
    - MCP_ACCESS_TOKEN: The access token you previously got
    - PIPEDREAM_PROJECT_ID: The project id of the Pipedream project you want to use
    - PIPEDREAM_ENVIRONMENT: The environment of the Pipedream project you want to use
3. Install dependencies: pip install agno mcp-sdk
"""

import asyncio
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.mcp import MCPTools, StreamableHTTPClientParams
from agno.utils.log import log_exception

app_slug = "google_calendar"

mcp_server_url = f"https://mcp.pipedream.net/324ab699-7034-4465-9298-56a0b7837997/{app_slug}"
mcp_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSJ9.eyJqdGkiOiI2NTBhY2Q2Yy04MjkxLTQ4Y2ItYjcxYi01Njk5NWE0ZDIwODYiLCJpc3MiOiJodHRwczovL2FwaS5waXBlZHJlYW0uY29tIiwiZXhwIjoxNzUxMjk2MjAwLCJpYXQiOjE3NTEyOTI2MDAsIm5iZiI6MTc1MTI5MjU5NSwidG9rZW5fdHlwZSI6Im9hdXRoX2FjY2Vzc190b2tlbiIsImF1ZCI6WyJhcGkiLCJjYXRjaGVyIl0sInN1YiI6Im9feUpJQXFweiIsInNjb3BlcyI6WyIqIl19.kdudI-bLEQNkL66UQ5Ogq76tSqHwlECaQc8QamIl1LjNsx1RYfD0WSN75-b7MIp1jWzycRGfHMDbQkD-AHGWBA"
pipedream_project_id = "proj_ELsZGq6"
pipedream_environment = "development"


server_params = StreamableHTTPClientParams(
    url=mcp_server_url,
    headers={
        "Authorization": f"Bearer {mcp_access_token}",
        "x-pd-project-id": pipedream_project_id,
        "x-pd-environment": pipedream_environment,
    },
)


async def run_agent(task: str) -> None:
    try:
        async with MCPTools(
            server_params=server_params, transport="streamable-http", timeout_seconds=20
        ) as mcp:
            agent = Agent(
                model=OpenAIChat(id="gpt-4.1-mini"),
                tools=[mcp],
                markdown=True,
            )
            await agent.aprint_response(message=task, stream=True)
    except Exception as e:
        log_exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(run_agent("list all calendars events"))
    