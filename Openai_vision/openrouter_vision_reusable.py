import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    """Encode image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, prompt="What's in this image?", model="google/gemma-3-27b-it"):
    """
    Analyze an image using OpenRouter vision models
    
    Args:
        image_path (str): Path to the image file
        prompt (str): Text prompt to send along with the image
        model (str): OpenRouter model ID to use
        
    Returns:
        dict: The JSON response from the API
    """
    # Get base64 image encoding
    base64_image = encode_image(image_path)
    
    # Create data URL
    image_url = f"data:image/jpeg;base64,{base64_image}"
    
    # OpenRouter API key from environment variables
    api_key = os.getenv("OPEN_ROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
    
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
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
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
    return response.json()

if __name__ == "__main__":
    # Example usage
    image_path = "Openai_vision/tesco-shopping-receipt-CNTYDX.jpg"
    result = analyze_image(
        image_path=image_path,
        prompt="Analyze this shopping receipt and tell me the total amount"
    )
    
    # Print full response
    print(result)
    
    answer = result["choices"][0]["message"]["content"]
    print("\nAnswer:")
    print(answer)
