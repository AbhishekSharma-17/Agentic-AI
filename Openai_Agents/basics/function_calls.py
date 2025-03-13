from agents import Agent, Runner, function_tool
import asyncio
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_current_datetime():
    from datetime import datetime
    return datetime.now().strftime("%A, %Y-%m-%d %H:%M:%S")


@function_tool
def create_file(filename: str, content: str) -> str:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Error creating file '{filename}': {e}"

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
    name="Abhishek",
    instructions="You are a knowledgeable assistant capable of providing information and answering questions..",
    tools=[get_current_datetime, create_file, web_search]
)

async def main():
    
    result1 = await Runner.run(agent, input="who won champions trophy 2025 , create a comprehensive report analysing it in a markdwon file also put in the day and date when the file created")
    print(result1.raw_responses)
    print(result1.final_output)


if __name__ == "__main__":
    asyncio.run(main())
