import os
from agno.agent import Agent
from agno.tools.aws_lambda import AWSLambdaTools
from dotenv import load_dotenv

load_dotenv()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

# Create an Agent with the AWSLambdaTool
agent = Agent(
    tools=[AWSLambdaTools(region_name="us-east-1")],
    name="AWS Lambda Agent",
    show_tool_calls=True,
)

while True:  
    print("AWS Lambda Agent 🤖")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("AWS Agent: Goodbye! ✌🏻") 
        break
    
    agent.print_response(user_input, stream=True, markdown=True)