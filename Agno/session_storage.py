from agno.agent import Agent
from agno.storage.mongodb import MongoDbStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
from rich.pretty import pprint
import typer
import os

load_dotenv()

# MongoDB connection settings
db_url = os.getenv("DB_URL")
db_name = os.getenv("DB_NAME")
user_id = "Abhishek"
storage = MongoDbStorage(
            collection_name="agent_sessions", db_url=db_url, db_name=db_name
        )

def test_agent():
    existing_sessions = storage.get_all_session_ids(user_id=user_id)
    print(f"Existing Sessions: {existing_sessions}")
    if len(existing_sessions) > 0:
            session_id = existing_sessions[0]
    
    agent = Agent(
        storage=storage,
        tools=[DuckDuckGoTools()],
        # add_history_to_messages=True,
        user_id=user_id,
        show_tool_calls=True,
        read_chat_history=True,
        # num_history_runs=4,
        session_id=session_id,
    )
    if session_id is None:
            session_id = agent.session_id
            print(f"Started Session: {session_id}\n")
    else:
            print(f"Continuing Session: {session_id}\n")
            
    agent.print_response("what were we taking about the productivity tool can you name it", stream=True)
# pprint(agent.get_messages_for_session()

if __name__ == "__main__":
    typer.run(test_agent)