from agno.agent import Agent
from agno.tools.sql import SQLTools

db_url = "postgresql://neondb_owner:npg_pv1rNQUIFD3L@ep-wandering-smoke-a5ubc1ak-pooler.us-east-2.aws.neon.tech/raone?sslmode=require"

agent = Agent(tools=[SQLTools(db_url=db_url)])

while True:  
    print("SQL Agent 🤖")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("SQL Agent: Goodbye! ✌🏻") 
        break
    
    agent.print_response(user_input, stream=True, markdown=True)