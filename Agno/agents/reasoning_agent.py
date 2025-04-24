from agno.agent import Agent
from agno.team.team import Team
from agno.models.aws import AwsBedrock
from agno.models.openrouter import OpenRouter
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools
from agno.tools.exa import ExaTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.tavily import TavilyTools
from agno.tools.newspaper4k import Newspaper4kTools
from pydantic import BaseModel, Field
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

#Schemas
# class FinalSteps(BaseModel):
#   """Final Team Agent Structured Output"""
#   claim: str = Field(..., description="The factual claim that was extracted and verified.")
#   verdict: str = Field(..., description="Verdict on the claim: should be one of ['True', 'False', 'Uncertain'].")
#   explanation: str = Field(..., description="Brief rationale (2–3 sentences) for the verdict based on evidence.")
#   citations: List[str] = Field(..., description="List of URLs or citation references used to verify the claim.More the citations the better it is ")
#   confidence: float = Field(..., description="Confidence score (0 to 1) indicating the reliability of the verdict.")

# class FinalResponse(BaseModel):
#   """Final Team Agent Structured Output"""
#   claims: Optional[List[FinalSteps]] = Field(..., description="List of all verified claims with verdicts and evidence.")

web_search_agent = Agent(
    name="Web Searcher",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[TavilyTools(api_key=os.getenv('TAVILY_API_KEY'), 
                       search_depth="advanced"
                       )
           ],
    description="An AI Agent which is used when we have to do a web search to find relevant information from web",
    instructions="Get latest information from the web",
    show_tool_calls=False,
    markdown=True,
    add_datetime_to_instructions=True,
)

deep_search_agent = Agent(
    name="Diverse Web Searcher",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[ExaTools(api_key=os.getenv('EXA_API_KEY'),show_results=True)
           ],
    
    description="This is a deep search agent that performs diverse, comprehensive searches across multiple topics, domains, and perspectives",
    instructions=[
        # Core Query Diversification
        "When receiving a query, decompose it into multiple related search angles",
        "For each query, identify at least 3 distinct topic categories the query might belong to",
        "Generate separate searches for each identified category to ensure topical diversity",
        "Ensure results span different information types: facts, opinions, analyses, tutorials, examples",
        
        # Domain and Source Diversity
        "Distribute searches across varied domains: academic (.edu), commercial (.com), organizational (.org)",
        "Include diverse publication types: blogs, research papers, news sites, forums, documentation",
        "Balance mainstream and niche sources to capture both popular and specialized perspectives",
        "Incorporate international sources when relevant to gain global perspectives",
        
        # Temporal Diversity
        "Include time-stratified results: recent (past week), moderately recent (past year), established (past 5 years)",
        "Highlight trending discussions alongside established information",
        "For evolving topics, prioritize showing how information/opinions have changed over time",
        
        # Content Format Diversity
        "Retrieve diverse content formats: articles, datasets, code repositories, multimedia discussions",
        "When relevant, include visual content sources alongside text-based information",
        "Seek out interactive resources (tools, calculators, simulations) related to the query",
        
        # Perspective Diversity
        "For subjective topics, ensure representation of multiple viewpoints",
        "Include both mainstream consensus and alternative perspectives when they exist",
        "Present opposing viewpoints for controversial topics",
        
        # Search Process Implementation
        "For each query, generate at least 2 alternative phrasings to capture different semantic angles",
        "Always include specialized domain-specific sources when the query relates to technical fields",
        "Present results in categorized sections that highlight the diversity dimensions explored",
        "Always do breadth search across multiple topics rather than depth search on a single topic"
    ],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=True,
)

news_search_agent = Agent(
        name="News Searcher",
        model=OpenAIChat(id="gpt-4.1-mini"),
        tools=[ExaTools(
            include_domains=["cnbc.com", "reuters.com", "bloomberg.com", "aninews.in", "indiatoday.in", "aajtak.in", "linkedin.com"],
        )],
        description="An AI Agent which is used when we have to do a find news articles from credible news websites",
        instructions=["Search for news articles","Get latest information from the news"],
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
    )


news2_agent = Agent(tools=[Newspaper4kTools()], 
                    name="News Searcher 2",
              description = "This the secondary news agent which is used when we have to do a find news articles from credible news websites",
              instructions=["Search for news articles","Get latest information from the news"],
              show_tool_calls=True,
              markdown=True,
              model=OpenAIChat(id="gpt-4.1-mini")
              )


wikipedia_agent = Agent(tools=[WikipediaTools()], 
                        name="Wikipedia Searcher",
                        show_tool_calls=True, 
                        description="An AI Agent which is used when we have to do a find information from wikipedia", instructions=["Search for information on wikipedia"], 
                        markdown=True, 
                        add_datetime_to_instructions=True, )


# Monitor

monitor_agent = Team(
    mode = "coordinate",
    members=[web_search_agent, deep_search_agent, news_search_agent, news2_agent, wikipedia_agent],
    name="Fact-Check Team",
    model=AwsBedrock(
                    id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    aws_region="us-east-1",
                     ),
    # model=OpenAIChat(id="gpt-4.1"),
    tools=[
        ReasoningTools(add_instructions=True)
    ],
    description="An AI Fact checker who will Orchestrate, monitor and decide which AI Agent to use for a given task",
    instructions=[
        "Analyze the user query and beak into subtasks",
        "Decide which AI Agent to use for each subtask",
        "Check if there are multiple claims in the input",
        "Execute the AI Agent for each subtask",
        "verify the results of each subtask",
        "combine the results of each subtask to get the final result",
        "return the final result to the user",
        "Always use the reasoning tool to analyze the user query and break it into subtasks",
        "Always use reasoning tool to make a decision",
        "Always use reasoning tool to combine the results of each subtask",
        "Always use reasoning tool to verify the results of each subtask",
        "Always use deep Diverse Web Searcher agent atlest once in the process",
        "Do not generate resposne until you have substansial information to identify the claim as fact or false",
        "If there are multiple claims in the input, generate multiple output for each claim",
    ],
    markdown=True,
    add_datetime_to_instructions=True,
    # response_model=FinalResponse,
    enable_agentic_context=True,
    add_member_tools_to_system_message=True,
    share_member_interactions=True,
    show_tool_calls=True,
    enable_agentic_memory=True,
    expected_output=""" <Note>If input has multiple claims generate multiple results. Do not add any comments , suggestion , opening or closing statements</note>
    {
    claims=[
        (
            claim=“claim extrcated”,
            verdict=“verdict generated”,
            explanation=“explanation”,
            citations=[
                “https://example.com”,
                “”https://example.com”
            ],
            confidence=0.89
        ),
        (
            claim=“claim extrcated”,
            verdict=“verdict generated”,
            explanation=“explanation”,
            citations=[
                “https://example.com”,
                “”https://example.com”
            ],
            confidence=0.89
        )]}
    """,
)

monitor_agent.print_response(
    "recent tragedy in india 50 people died in terror attact",
    stream=True,
    show_full_reasoning=True,
    stream_intermediate_steps=True,
)
