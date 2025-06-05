from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.playground import Playground, serve_playground_app
import os
from dotenv import load_dotenv
from agno.tools.shell import ShellTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.dalle import DalleTools
from agno.tools.sql import SQLTools

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

modellabs_api_key ="qmQzHPJ2tSeyhPqDTWJIRs8qd1tWNSC81ZK8Ec8Js1BPAFzN3RLWvBSSeSIr"

db_url = "postgresql://neondb_owner:npg_pv1rNQUIFD3L@ep-wandering-smoke-a5ubc1ak-pooler.us-east-2.aws.neon.tech/raone?sslmode=require"

shell_agent = Agent(tools=[ShellTools()], 
              show_tool_calls=True, 
              name="Shell Agent", 
              description="You are an AI agent that can run shell commands on a MacOS machine.",
              instructions=["You are capable of generating and executing shell commands on macos and Windows and linux"], 
              enable_agentic_memory=True, 
              add_datetime_to_instructions=True,
              add_history_to_messages=True,
              num_history_responses=2)

web_agent = Agent(
    name="web_agent",
    role="search the web for information",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[DuckDuckGoTools()],
    instructions="Always include sources",
     show_tool_calls=True,
     markdown=True
)


sql_agent = Agent(tools=[SQLTools(db_url=db_url)],
                  description="You are an AI agent that can query a SQL database.",
                  instructions=["You are capable of generating and executing SQL queries on a SQL database"],
                  enable_agentic_memory=True,
                  add_datetime_to_instructions=True,
                  name="SQL Agent",
                  add_history_to_messages=True,
                  num_history_responses=2
                  )

finance_agent = Agent(
    name="finance_agent",
    role="get finance data",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools(enable_all=True)],
    instructions="use tables to display data",
     show_tool_calls=True,
     markdown=True
)

image_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[DalleTools(quality="hd")],
    name="Image Agent",
    description="You are an AI agent that can generate images using DALL-E.",
    instructions="When the user asks you to create an image, use the `create_image` tool to create the image.",
    markdown=True,
    show_tool_calls=True,
)

wikipedia_agent = Agent(tools=[WikipediaTools()], 
                        name="Wikipedia Searcher",
                        show_tool_calls=True, 
                        description="An AI Agent which is used when we have to do a find information from wikipedia", instructions=["Search for information on wikipedia"], 
                        markdown=True, 
                        add_datetime_to_instructions=True, )

audio_agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "pcm16"},  # 'mp3', 'opus', 'aac', 'flac', 'wav', and 'pcm16'.
    ),
    markdown=True,
        name="Audio Agent",
    description="You are an agent capable of genearting audio"
)


finance_team = Team(
    members=[web_agent, finance_agent, wikipedia_agent],
    model=OpenAIChat(id="gpt-4.1"),
    name="Finance Team",
    tools=[
        ReasoningTools(add_instructions=True)
    ],
    mode="collaborate",
    instructions=["Always include sources","use tables to display data",
                  "Use the reasoning tool to decide which agent to use for a given task",
                  ],
    add_datetime_to_instructions=True,
     show_tool_calls=True,
     markdown=True
)
image_team = Team(
    members=[web_agent, image_agent, wikipedia_agent],
    mode="coordinate",
    name="Image Team",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[
        ReasoningTools(add_instructions=True)
    ],
    instructions=["Do the research on given topic and then generate an image",
                  "Use the reasoning tool to decide which agent to use for a given task",
                  "When the user asks you to create an image, use the `create_image` tool to create the image.",
                  "do good research and comup with a response"
                  ],
     show_tool_calls=True,
     markdown=True
)




app = Playground(
    agents=[finance_agent, web_agent, shell_agent, sql_agent, wikipedia_agent, image_agent, audio_agent ],
    teams=[finance_team, image_team]
).get_app()

if __name__ == "__main__":
    serve_playground_app("playground_testing:app", reload=True)
    