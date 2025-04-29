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
    instructions=["give the video content just as it is word by word",
                  "The output should be in english",
                  "If the video is in any other language translate it to english",
                  "The meaning of the video should be preserved when translated in english",
                  "Do not add any comments, symbols  or anything else in the output",
                  "The words and sentences statement should also be in english"
                  ],
    description="This agent is used to convert videos to text in english",
)


video_path = Path(__file__).parent.joinpath("hindi_news.mp4")

with open(video_path, "rb") as video_file:

    video_data = video_file.read()
# response = agent.run("Tell me about this video", videos=[Video(content=video_data, format="mp4")])

# print(response.content)

response = agent.run("give the video content just as it is word by word in English", videos=[Video(content=video_data, format="mp4")],stream=True)

for res in response:
    print(res.content, end="", flush=True)
