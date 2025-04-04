from pathlib import Path
import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.media import Video
from agno.models.google import Gemini

load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp",api_key=os.getenv("GEMINI_API_KEY")),
    markdown=True,
)


video_path = Path(__file__).parent.joinpath("test.mp4")

with open(video_path, "rb") as video_file:

    video_data = video_file.read()
# response = agent.run("Tell me about this video", videos=[Video(content=video_data, format="mp4")])

# print(response.content)

response = agent.run("explain the", videos=[Video(content=video_data, format="mp4")],stream=True)

for res in response:
    print(res.content, end="", flush=True)
