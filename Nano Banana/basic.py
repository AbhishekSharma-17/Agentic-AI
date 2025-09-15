#!/usr/bin/env python3
"""
Simple Nano Banana (Gemini 2.5 Flash Image) Text-to-Image Generator
Uses OpenRouter API for image generation
"""

import os
import base64
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt, api_key=None, output_path=None):
    """
    Generate image from text prompt using Nano Banana (Gemini 2.5 Flash Image)

    Args:
        prompt (str): Text description for image generation
        api_key (str): OpenRouter API key (optional if set in environment)
        output_path (str): Path to save image (optional)

    Returns:
        str: Path to saved image file or None if failed
    """
    # Get API key
    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("❌ Error: No API key provided. Set OPENROUTER_API_KEY environment variable or pass api_key parameter.")
        return None

    # API configuration
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "google/gemini-2.5-flash-image-preview",
        "messages": [
            {
                "role": "user",
                "content": "Generate and image for " + prompt
            }
        ],
        "modalities": ["image"]
    }

    try:
        print(f"🎨 Generating image for: '{prompt}'")
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract image from response
        if "choices" in result and len(result["choices"]) > 0:
            message = result["choices"][0]["message"]

            if "images" in message:
                # Get base64 image data
                image_data = message["images"][0]["image_url"]["url"]

                # Remove data URL prefix if present
                if image_data.startswith("data:image"):
                    image_data = image_data.split(",", 1)[1]

                # Generate output path if not provided
                if not output_path:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    os.makedirs("generated_images", exist_ok=True)
                    output_path = f"generated_images/nano_banana_{timestamp}.png"

                # Decode and save image
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                image.save(output_path)

                print(f"✅ Success! Image saved to: {output_path}")
                return output_path

            elif "content" in message:
                print(f"📝 Got text response instead of image: {message['content']}")
                return None

        print("❌ No image found in response")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Simple CLI interface"""
    print("🍌 Nano Banana Image Generator")
    print("=" * 40)

    # Check for API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("🔑 No OPENROUTER_API_KEY found in environment.")
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print("❌ No API key provided. Exiting.")
            return

    # Get prompt from user
    while True:
        prompt = input("\n🎨 Enter your image prompt (or 'quit' to exit): ").strip()

        if prompt.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not prompt:
            print("❌ Please enter a valid prompt")
            continue

        # Generate image
        result = generate_image(prompt, api_key)

        if result:
            print(f"🎉 Image generated successfully!")
        else:
            print("💥 Failed to generate image. Please try again.")


if __name__ == "__main__":
    # Example usage when run directly
    if len(os.sys.argv) > 1:
        # Command line usage: python nano_banana_simple.py "your prompt here"
        prompt = " ".join(os.sys.argv[1:])
        result = generate_image(prompt)
        if result:
            print(f"Image saved to: {result}")
    else:
        # Interactive mode
        main()