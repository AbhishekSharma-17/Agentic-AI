from sarvamai import SarvamAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(
    api_subscription_key=api_key,
)

current_dir = os.path.dirname(os.path.abspath(__file__)) 
audio_file_path = os.path.join(current_dir, 'test.wav')

response = client.speech_to_text.translate(
    file=open(audio_file_path, "rb"),
    model="saaras:v2"

)

print(response.transcript)
