from agno.agent import Agent
from agno.tools.youtube import YouTubeTools

agent = Agent(
    tools=[YouTubeTools(get_video_captions=True, get_video_data=True)],
    show_tool_calls=True,
    description="You are a YouTube agent. Obtain detailed summary.",
    instructions=["Generate detailed summary of the video."],     
)

agent.print_response("https://youtu.be/mRxnXiZDmVM?si=zbUoJScE2Yldqlf9", markdown=True)