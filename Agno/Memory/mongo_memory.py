from agno.agent.agent import Agent
from agno.memory.v2.db.mongodb import MongoMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.mongodb import MongoDbStorage

DATABASE_URL='mongodb+srv://priyanshu:ZU0oUag2Tyu9jmNK@krooloprod.u99kr.mongodb.net/qastage01?retryWrites=true&w=majority'
DB_NAME='qastage01'

memory = Memory(db=MongoMemoryDb(collection_name="agent_memories", db_url=DATABASE_URL,db_name=DB_NAME), 
                model=OpenAIChat(id="gpt-4.1-nano"),
                debug_mode=True)

session_id = "mongodb_memories"
user_id = "6808c7e4e7f831e6a1026542"

agent = Agent(
    model=OpenAIChat(id="gpt-4.1-mini"),
    memory=memory,
    storage=MongoDbStorage(collection_name="agent_sessions", db_url=DATABASE_URL, db_name=DB_NAME),
    # enable_user_memories=True,
    enable_agentic_memory=True,
    user_id=user_id,
    # session_id=session_id
    enable_session_summaries=True,
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    agent.print_response(user_input, stream=True)

 