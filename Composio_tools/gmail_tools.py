from agno.agent.agent import Agent
from composio_agno import Action, App, ComposioToolSet
import os
from dotenv import load_dotenv


load_dotenv()


toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

gmail_tools = toolset.get_tools(actions=["GMAIL_LIST_DRAFTS", "GMAIL_GET_ATTACHMENT","GMAIL_SEND_EMAIL"])



agent = Agent(tools=gmail_tools, show_tool_calls=True, add_datetime_to_instructions=True, 
              add_history_to_messages=True,
              num_history_responses=4
              )


while True:  
    print("Gmail Agent 🤖")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("Gmail Agent: Goodbye! ✌🏻")
        break
    
    agent.print_response(user_input, stream=True, markdown=True)
