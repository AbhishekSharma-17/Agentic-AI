import json
import os
import uvicorn
from dotenv import load_dotenv
from agno.models.openai import OpenAIChat
from agno.agent.agent import Agent
from agno.tools.exa import ExaTools
from agno.tools.reasoning import ReasoningTools
from agno.team.team import Team
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import AsyncGenerator , cast
from agno.run.response import RunEvent
from agno.run.team import TeamRunResponse

load_dotenv()

# app = FastAPI()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # Allows all origins for testing
#     allow_credentials=True,
#     allow_methods=["*"], # Allows all methods
#     allow_headers=["*"], # Allows all headers
# )

# Research specialist for gathering accurate information
research_agent = Agent(
    name="Research Specialist",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[ExaTools(api_key=os.getenv('EXA_API_KEY'), show_results=True,num_results=2)],
    description="Information gathering specialist who collects accurate, current and relevant data on specified topics",
    instructions=[
        "Research current information on the specified topic using search tools",
        "Gather data for all required document sections: Business Context, Technical Perspective, etc.",
        "Collect industry or organizational landscape information",
        "Identify key challenges, trends, and opportunities",
        "Research potential architectural approaches and technologies",
        "Find relevant case studies and implementation examples",
        "Gather statistical data on benefits and outcomes where available",
        "Use the exa tool to do web search to find relevant information",
        "Provide source attribution for all information",
        "Prioritize most recent and latest information",
        "check for the current date and time provided"
    ],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=True,
)

# Content creator for drafting the POV document
pov_writer = Agent(
    name="POV Writer",
    model=OpenAIChat(id="gpt-4.1-mini"),
    description="Technical content creation specialist who drafts detailed, factual POV documents with a focus on business value and technical insights",
    instructions=[
        "Draft content for each section of the POV document based on research findings",
        "Create content that balances technical accuracy with business value",
        "Maintain third-person perspective for credibility",
        "Define problems clearly with technical context in the Technical Perspective section",
        "Present architectural approaches with concrete details and rationales",
        "Articulate specific, measurable benefits and outcomes",
        "Provide realistic implementation considerations and roadmaps",
        "Include relevant case studies with tangible results",
        "Develop actionable recommendations and next steps",
        "Support all claims with evidence and data points from research",
        "Use technical terminology appropriately for the intended audience",
        "Balance depth with accessibility for technical decision-makers"
    ],
    show_tool_calls=False,
    markdown=True,
    add_datetime_to_instructions=True,
)

# Format and structure specialist
pov_formatter = Agent(
    name="POV Formatter",
    model=OpenAIChat(id="gpt-4.1-mini"),
    description="Document architecture specialist who structures and formats enterprise-grade POV documents according to standardized templates",
    instructions=[
        "Structure document according to the enterprise POV template with these sections:",
        "- Title: Short, clear, outcome-driven",
        "- Executive Summary: Context, proposal, value, audience (2-3 paragraphs)",
        "- Business Context: Industry landscape, challenges, trends, urgency",
        "- Technical Perspective: Problem definition, pain points, tech opportunities",
        "- Proposed Approach/Architecture: Methodology, architecture, tools, patterns",
        "- Benefits & Outcomes: Technical/business gains, efficiencies, risk reduction",
        "- Implementation Considerations: Phases, resources, risks, dependencies",
        "- Industry Use Cases: 1-2 examples with technologies and benefits",
        "- Recommendations & Next Steps: Key actions, workshops, POC, timeline",
        "- Appendix (Optional): Reference architectures, tool comparisons, glossary",
        "Use bullet points for clarity in appropriate sections",
        "Create professional, scannable formatting throughout",
        "Ensure consistent heading hierarchy and formatting",
        "Format case studies and technical details for maximum readability",
        "Structure content to emphasize business value alongside technical details",
        "Create a compelling title that highlights transformation and outcomes"
    ],
    show_tool_calls=False,
    markdown=True,
    add_datetime_to_instructions=True,
)

# Orchestrator with enhanced coordination for enterprise POV documents
pov_team = Team(
    mode="coordinate",
    members=[research_agent, pov_writer, pov_formatter],
    name="Enterprise POV Team",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[
        ReasoningTools()
    ],
    description="Multi-agent team for creating enterprise-grade technical POV documents that provide business and technical insights on emerging technologies and solutions",
    instructions=[
        "ANALYSIS PHASE:",
        "1. Analyze user query to determine the specific technical domain and business context",
        "2. Use reasoning tools to identify key topics requiring research across all POV sections",
        "3. Create a research plan covering business context through recommendations",
        
        "RESEARCH PHASE:",
        "4. Task Research Specialist to gather comprehensive information for all sections",
        "5. Ensure research covers industry context, technical details, and implementation examples",
        "6. Review research for completeness across all required sections",
        
        "CONTENT CREATION PHASE:",
        "7. Task POV Writer to draft content for each document section",
        "8. Ensure technical accuracy while maintaining business focus",
        "9. Review section content for alignment with enterprise POV standards",
        
        "STRUCTURE PHASE:",
        "10. Task POV Formatter to organize content according to the enterprise template",
        "11. Ensure proper formatting for all sections from title through appendix",
        "12. Review structure for professional presentation and readability",
        
        "QUALITY CONTROL PHASE:",
        "13. Verify technical accuracy and business relevance across all sections",
        "14. Ensure appropriate depth for executive and technical audiences",
        "15. Check that all sections connect logically from problem to solution to implementation",
        "16. Confirm sources are properly integrated and support key claims",
        
        "DELIVERY PHASE:",
        "17. Compile final enterprise POV document with consistent formatting",
        "18. Format the final document enterprise POV structure:"
    ],
    markdown=True,
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    share_member_interactions=True,
    show_tool_calls=True,
    enable_agentic_memory=True,
    expected_output="""
    "    # [TITLE]",
        "    ",
        "    ## Executive Summary",
        "    [2-3 paragraphs explaining context, proposal, value, and intended audience]",
        "    ",
        "    ## Business Context",
        "    [Industry landscape, key challenges, trends, urgency, what's at stake]",
        "    ",
        "    ## Technical Perspective",
        "    [Problem definition, technical pain points, opportunities for improvement]",
        "    ",
        "    ## Proposed Approach/Architecture",
        "    [Methodology, architecture, tools/platforms, design patterns/principles]",
        "    ",
        "    ## Benefits & Outcomes",
        "    [Technical and business outcomes, efficiency gains, risks mitigated]",
        "    ",
        "    ## Implementation Considerations",
        "    [Phases/roadmap, resource needs, risks/mitigations, dependencies]",
        "    ",
        "    ## Industry Use Cases",
        "    [1-2 examples showing success in similar scenarios, technologies, benefits]",
        "    ",
        "    ## Recommendations & Next Steps",
        "    [Key recommendations, suggested actions, timeline]",
        "    ",
        "    ## Appendix (Optional)",
        "    [Reference architectures, tool comparisons, glossary/acronyms]",
        "    ",
        "    ## Sources",
        "    [List of references and citations, Links used throughout the document]"
    """
)

# class ChatRequest(BaseModel):
#     user_query: str

# @app.get("/")
# async def read_root():
#     return {"message": "Agentic AI FastAPI server is running"}

# @app.post("/pov-team")
# async def run_team_endpoint(request: ChatRequest):
   
#     async def team_chat_response_streamer(
#             team: Team,
#             message: str,
#         ) -> AsyncGenerator:
#         try:
#             run_response = await team.arun(
#                 message,
#                 stream=True,
#                 # stream_intermediate_steps=True,
#             )
#             async for run_response_chunk in run_response:
#                 run_response_chunk = cast(TeamRunResponse, run_response_chunk)
#                 if run_response_chunk.reasoning_content:
#                     yield "Reasoning:"
#                     yield run_response_chunk.reasoning_content
#                 if run_response_chunk.content:
#                     yield "content"
#                     yield run_response_chunk.content
                
                
#         except Exception as e:
#             error_response = TeamRunResponse(
#                 content=str(e),
#                 event=RunEvent.run_error,
#             )
#             yield error_response.to_json()
#             return
                    
#     return StreamingResponse(
#             team_chat_response_streamer(team=pov_team ,message=request.user_query), 
#             media_type="text/event-stream",
#             headers={
#                 "Cache-Control": "no-cache",
#                 "Connection": "keep-alive",
#             }
#         )


# if __name__ == "__main__":
#     uvicorn.run("Pov_agents:app", host="127.0.0.1", port=8000, reload=True)

while True:  
    print("\nPOV Agent 🤖")
    print("\n")
    user_input = input("You: ") 
    
    if user_input.lower() in ["exit", "q"]: 
        print("POV Agent: Goodbye! ✌🏻") 
        break

    pov_team.print_response(user_input, stream=True, markdown=True)