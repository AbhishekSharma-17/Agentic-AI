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
tools = toolset.get_tools(apps=[App.GOOGLECALENDAR])


agent = Agent(tools=tools, show_tool_calls=True, add_datetime_to_instructions=True, instructions=[f"Today is {datetime.datetime.now()} and the users timezone is {get_localzone_name()}",
                                        "List all the meetings and analyze the query and target correct meetings or evensts",
                                        "For example the meet title maybe Composio Integration but user says composio meet then it should understand the semantic meaning and choose the correct meeting"                                                          
                                                                                                  ])

# agent.print_response("Schedule a meeting with keshav , Email : keshav.garg@kroolo.com , Title should be composio Integration and timimg is 10 PM today , Also mention in the description That this created using Composio")

agent.print_response("Add vikas.kumar@kroolo.com in Composio meet") 