import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()                

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "Openai_vision/tesco-shopping-receipt-CNTYDX.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

# Creating the data URL
image_url = f"data:image/jpeg;base64,{base64_image}"

response = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": image_url,
            },
        ],
            
    }],
)

#while invoking
print(response.output_text)

