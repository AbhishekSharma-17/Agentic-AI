from agno.agent.agent import Agent
from composio_agno import Action, App, ComposioToolSet
import os
from dotenv import load_dotenv
from tzlocal import get_localzone_name
import datetime

load_dotenv()


toolset = ComposioToolSet(api_key=os.getenv("COMPOSIO_API_KEY"))

# request = toolset.initiate_connection(app=App.GITHUB)
# print(f"Open this URL to authenticate: {request.redirectUrl}")

# composio add googlecalendar this triggers oauth

# You can get all the tools for a given app
tools = toolset.get_tools(apps=[App.SLACK])


agent = Agent(tools=tools, show_tool_calls=True, add_datetime_to_instructions=True, instructions=[f"Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}",
                                        "you can do anything in slack"                                                    
                                                                                                  ],
              add_history_to_messages=True,
              num_history_responses=4
              )

# agent.print_response("Schedule a meeting with keshav , Email : keshav.garg@kroolo.com , Title should be composio Integration and timimg is 10 PM today , Also mention in the description That this created using Composio")

while True:  
    print("Slack Agent 🤖")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("Slack Agent: Goodbye! ✌🏻")
        break
    
    agent.print_response(user_input, stream=True, markdown=True)
