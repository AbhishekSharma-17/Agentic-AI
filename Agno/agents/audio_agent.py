import base64
from pathlib import Path
from agno.agent import Agent
from agno.media import Audio
from agno.models.openai import OpenAIChat

# Get the current file's directory and create path to audio file
current_dir = Path(__file__).parent
audio_path = str(current_dir / "test.wav")

# Read the audio file content directly
with open(audio_path, "rb") as audio_file:
    wav_data = audio_file.read()

# Create the agent with the appropriate model
agent = Agent(
    model=OpenAIChat(id="gpt-4o-audio-preview", modalities=["text"]),
    markdown=True,
)

# Pass the audio content directly instead of using filepath or base64 URL

print("Attempting to process audio using content method...")
response = agent.run(
    "What is in this audio?", audio=[Audio(content=wav_data, format="wav")]
)
response1 = agent.run(
    "where does abhihsek work?", audio=[Audio(filepath=audio_path, format="wav")]
)

print(response.content)
