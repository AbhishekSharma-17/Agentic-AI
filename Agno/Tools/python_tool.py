from agno.agent import Agent
from agno.tools.python import PythonTools
from dotenv import load_dotenv
from agno.models.openai import OpenAIChat

load_dotenv()



model = OpenAIChat(
    id="gpt-4.1",
)

agent = Agent(tools=[PythonTools(
    pip_install=True,
    uv_pip_install=True,
    run_code=True,
    run_files=True,
    save_and_run=True,
    list_files=True,
    read_files=True,
    )],
    show_tool_calls=True,
    markdown=True,
    name="Python Agent",
    description="You are an AI agent that can run python code on macos machine.",
    instructions=["You are capable of generating and executing python code","You can run python files","You can save and run python files","You can list files in the current directory","You can read files in the current directory","You can analyz the query and create python code and execute to get the result"],
    enable_agentic_memory=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=4,
    model=model,
    )

while True:  
    print("Manus Agent 🤖")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("Manus Agent: Goodbye! ✌🏻") 
        break
    
    agent.print_response(user_input, stream=True)