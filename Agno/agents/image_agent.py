from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
import base64
import os
from pathlib import Path

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    markdown=True,
)

# agent.print_response(
#     "Tell me about this image and give me the latest news about it.",
#     images=[
#         Image(
#             url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"
#         )
#     ],
#     stream=True,
# )

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Get the current file's directory and create path to image
current_dir = Path(__file__).parent
image_path = str(current_dir / "tesco-shopping-receipt-CNTYDX.jpg")

image_data = encode_image(image_path)

response = agent.run("explain this image", images=[Image(url="data:image/jpeg;base64," + image_data)])
#"url": "data:image/jpeg;base64,{image_data}"

response_1 = agent.run("explain this image", images=[Image(filepath=image_path)],stream=True)
# print(response_1.content) 

for res in response_1:
    print(res.content,flush=True,end="")
