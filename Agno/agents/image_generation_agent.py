from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.dalle import DalleTools
import datetime
import requests
import base64

image_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DalleTools(quality="hd")],
    description="You are an AI agent that can generate images using DALL-E.",
    instructions="When the user asks you to create an image, use the `create_image` tool to create the image.",
    markdown=True,
    show_tool_calls=True,
)

response = image_agent.run("image of a shampoo bottle named something hindi")

# images = image_agent.get_images()
# if images and isinstance(images, list):
#     for image_response in images:
#         image_url = image_response.url
#         print(image_url)

#  Get images from the agent response
images = image_agent.get_images()
if images and isinstance(images, list):
    for i, image_response in enumerate(images):
        image_url = image_response.url
        print(f"Image URL: {image_url}")
        
        # Create a timestamp for unique filenames
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save original image
            image_filename = f"generated_image_{timestamp}_{i}.png"
            with open(image_filename, "wb") as img_file:
                img_file.write(response.content)
            print(f"Image saved to {image_filename}")
            
            # Convert to base64
            base64_encoded = base64.b64encode(response.content).decode('utf-8')
            
            # Save base64 string to file
            base64_filename = f"base64_image_{timestamp}_{i}.txt"
            with open(base64_filename, "w") as b64_file:
                b64_file.write(base64_encoded)
            print(f"Base64 encoded data saved to {base64_filename}")

print(response)