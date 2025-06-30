from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.fal import FalTools
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FAL_KEY"] = os.getenv("FAL_KEY")
print(os.environ["FAL_KEY"])
fal_agent = Agent(
    name="Fal Video Generator Agent",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[FalTools(model="fal-ai/veo3",api_key=os.getenv("FAL_KEY"))],
    description="You are an AI agent that can generate videos using the Fal API.",
    instructions=[
        "When the user asks you to create a video, use the `generate_media` tool to create the video.",
        "Return the URL as raw to the user.",
        "Generate only one video",
        "Don't convert video URL to markdown or anything else.",
    ],
    markdown=True,
    debug_mode=True,
    show_tool_calls=True,
)

# fal_agent.print_response("Generate video of balloon in the ocean")

from agno.playground import Playground, serve_playground_app

app = Playground(
    agents=[fal_agent],
).get_app()

if __name__ == "__main__":
    serve_playground_app("fal_tool:app", reload=True)