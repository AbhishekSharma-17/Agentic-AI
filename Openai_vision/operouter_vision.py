import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

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

# OpenRouter API key from environment variables
api_key = os.getenv("OPEN_ROUTER_API_KEY")
print(api_key)

# OpenRouter API endpoint
url = "https://openrouter.ai/api/v1/chat/completions"

# Headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://localhost",  # Required by OpenRouter
}

# Request payload
payload = {
    "model": "google/gemma-3-27b-it",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }
    ]
}

# Make the API request
response = requests.post(url, json=payload, headers=headers)

# Print the full JSON response
print("Full response:")
print(response.json())

# Extract and print just the text content from the response
if "choices" in response.json() and len(response.json()["choices"]) > 0:
    answer = response.json()["choices"][0]["message"]["content"]
    print("\nAnswer text only:")
    print(answer)
