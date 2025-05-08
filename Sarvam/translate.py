import os
from sarvamai import SarvamAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(
    api_subscription_key=api_key,
    )

response = client.text.translate(
    input="Hi my name is Abhishek",
    source_language_code="auto",
    target_language_code="hi-IN",
    speaker_gender="Male"
)

print(response)