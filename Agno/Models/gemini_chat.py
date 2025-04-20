from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

load_dotenv()

# Using Google AI Studio
agent = Agent(
    model=Gemini(id="gemini-2.0-flash",api_key=os.getenv("GEMINI_API_KEY"),
                 grounding=True, #Provides grounding to the model , add sources
                 search=True, #Provides web search capabilities
                 ),
    show_tool_calls=True,
    markdown=True,
)

# Or using Vertex AI
# agent = Agent(
#     model=Gemini(
#         id="gemini-2.0-flash",
#         vertexai=True,
#         project_id="your-project-id",  # Optional if GOOGLE_CLOUD_PROJECT is set
#         location="us-central1",  # Optional
#     ),
#     markdown=True,
# )

# Print the response in the terminal
agent.print_response("what is agno framework")