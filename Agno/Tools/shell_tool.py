from agno.agent import Agent
from agno.tools.shell import ShellTools

agent = Agent(tools=[ShellTools()], show_tool_calls=True, name="Macos Shell Agent", description="You are an AI agent that can run shell commands on a MacOS machine.",instructions=["You are capable of generating and executing shell commands on macos"], enable_agentic_memory=True, add_datetime_to_instructions=True,add_history_to_messages=True,num_history_responses=2)


while True:  
    print("Shell Agent: What can I do for you?")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "quit"]: 
        print("Shell Agent: Goodbye!") 
        break
    
    agent.print_response(user_input, stream=True) 
