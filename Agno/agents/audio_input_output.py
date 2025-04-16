import os
from pathlib import Path
from agno.agent import Agent
from agno.media import Audio
from agno.models.openai import OpenAIChat
from agno.utils.audio import write_audio_to_file

# Get the current file's directory and create path to audio file
current_dir = Path(__file__).parent
audio_path = str(current_dir / "test.wav")

# Read the audio file content directly
with open(audio_path, "rb") as audio_file:
    wav_data = audio_file.read()

agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
    ),
    markdown=True,
)

agent.run("What's in these recording?", audio=[Audio(content=wav_data, format="wav")])

# Create tmp directory if it doesn't exist
if not os.path.exists("tmp"):
    os.makedirs("tmp")

if agent.run_response.response_audio is not None:
    write_audio_to_file(
        audio=agent.run_response.response_audio.content, filename="tmp/result.wav"
    )
