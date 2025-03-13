from agents import Agent, function_tool, Runner
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

@function_tool
def web_search(query: str) -> str:
    
    try:
        tool = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
        )
        results = tool.run(query)
        return results
    except Exception as e:
        return f"Error performing web search: {str(e)}"

agent = Agent(
    name="AI Abhi",
    instructions="You are an AI assistant designed to help users with their queries. Provide clear, concise, and helpful responses for a wide range of topics.",
    model="-gpt-4o-mini",
    tools=[web_search]
)

result = Runner.run_sync(agent, "what is weather in jehanabd and cuurret day and date")

print(result.final_output)