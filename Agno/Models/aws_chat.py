import os
from agno import agent
from agno.agent.agent import Agent
from agno.models.aws import AwsBedrock
from dotenv import load_dotenv

load_dotenv()

llm = AwsBedrock(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                 aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                 aws_region="us-east-1",
                 id="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
)
agent = Agent(
    model=llm,
    markdown=True
)

agent.print_response("Who are you?")
