from sarvamai import SarvamAI
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(
    api_subscription_key=api_key,
)

response = client.text_to_speech.convert(
    inputs=["Hello, how are you?"],
    target_language_code="hi-IN",
)

print(response.audios)
