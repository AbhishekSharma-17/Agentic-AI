import base64
from openai import OpenAI
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# OpenRouter uses chat completions endpoint for image generation
response = client.chat.completions.create(
    model="google/gemini-2.5-flash-image-preview",
    messages=[
        {
            "role": "user",
            "content": "a portrait of a sheepadoodle wearing a cape"
        }
    ],
    modalities=["image", "text"]
)

# Extract and display the generated images
if response.choices and response.choices[0].message.images:
    for image_data in response.choices[0].message.images:
        # Extract base64 data from the data URL
        # Handle both dict and object attribute access
        if hasattr(image_data, 'image_url'):
            url = image_data.image_url.url
        else:
            url = image_data['image_url']['url']
        
        base64_data = url.split(',')[1]
        image = Image.open(BytesIO(base64.b64decode(base64_data)))
        image.save(f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
else:
    print("No images were generated in the response")
