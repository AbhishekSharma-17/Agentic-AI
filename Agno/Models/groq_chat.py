from agno.agent import Agent, RunResponse
from agno.models.groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY")),
    markdown=True
)

# Print the response in the terminal
agent.print_response("What is ai ?")