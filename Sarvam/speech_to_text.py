from sarvamai import SarvamAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(
    api_subscription_key=api_key,
)

current_dir = os.path.dirname(os.path.abspath(__file__)) 
audio_file_path = os.path.join(current_dir, 'test.wav')

response = client.speech_to_text.transcribe(
    file=open(audio_file_path, "rb"),
    model="saarika:v2",
    language_code="mr-IN"
)

print(response)
