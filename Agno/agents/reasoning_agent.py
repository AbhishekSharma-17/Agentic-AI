from agno.agent import Agent
from agno.models.aws import AwsBedrock
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.exa import ExaTools
from dotenv import load_dotenv
import os

load_dotenv()

agent = Agent(
    model=AwsBedrock(
                    id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    aws_region="us-east-1",
                     ),
    # model=OpenAIChat(id="o4-mini-2025-04-16"),
    tools=[
        ReasoningTools(add_instructions=True),
        ExaTools(api_key=os.getenv("EXA_API_KEY"),)
    ],
    instructions=[
        "Use tables to display data.",
        "Include sources in your response.",
        "Only include the report in your response. No other text.",
    ],
    markdown=True,
)
agent.print_response(
    "Write a report on Kroolo",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True,
)