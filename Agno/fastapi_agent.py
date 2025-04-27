from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware # Import CORS Middleware
from agno.agent import Agent
from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.models.aws import AwsBedrock
from agno.tools.tavily import TavilyTools
from agno.tools.reasoning import ReasoningTools
from pydantic import BaseModel
import os
import uvicorn
import json # Import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

web_search_agent = Agent(
    name="Web Searcher",
    model=OpenAIChat(id="gpt-4o-mini"),
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

monitor_agent = Team(
    mode = "coordinate",
    members=[web_search_agent],
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
        "Do not generate resposne until you have substansial information to identify the claim as fact or false",
        "If there are multiple claims in the input, generate multiple output for each claim",
        """The final output should be a JSON object with the following fields:
        - claim: The factual claim that was extracted and verified.
        - verdict: Verdict on the claim: should be one of ['True', 'False'].
        - explanation: Brief rationale (2–3 sentences) for the verdict based on evidence.
        - Confidence: Confidence score (0 to 1) indicating the reliability of the verdict.
        """,
        "In the final output follow the given format and do not add any extra fields",
        
    ],
    markdown=True,
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    add_member_tools_to_system_message=True,
    share_member_interactions=True,
    show_tool_calls=True,
    debug_mode=True,
    expected_output=""" Return a JSON object with the following fields:
    - claim: The factual claim that was extracted and verified.
    - verdict: Verdict on the claim: should be one of ['True', 'False', 'Uncertain'].
    - explanation: Brief rationale (2–3 sentences) for the verdict based on evidence.
    - Confidence: Confidence score (0 to 1) indicating the reliability of the verdict.
    
    <Important>Apart from this json object do not generate any other suggestion , comments , opening or closing statements. Just the json object</Important>
    """,
)

class ChatRequest(BaseModel):
    user_query: str

@app.get("/")
async def read_root():
    return {"message": "Agentic AI FastAPI server is running"}


# New endpoint for running the team and streaming the response
@app.post("/run-team")
async def run_team_endpoint(request: ChatRequest):
    """Endpoint to run the monitor_agent team and stream results as NDJSON."""
    # Generator function to stream the agent's response as JSON
    async def stream_agent_response_json(query: str):
        """Runs the monitor_agent and yields JSON response chunks."""
        # Make sure to request intermediate steps and reasoning
        response_stream = monitor_agent.run(
            query,
            stream=True,
            show_full_reasoning=True, # Ensure this is True
            stream_intermediate_steps=True # Ensure this is True
        )
        for chunk in response_stream:
            try:
                # Convert the Agno response object (likely Pydantic) to a dict, then to JSON
                # Use model_dump() for Pydantic v2+ or dict() for older versions if needed
                if hasattr(chunk, 'model_dump'):
                    chunk_dict = chunk.model_dump(mode='json')
                elif hasattr(chunk, 'dict'):
                     chunk_dict = chunk.dict()
                else:
                     # Fallback or handle non-Pydantic objects if necessary
                     chunk_dict = {"event": "UnknownChunk", "content": str(chunk)}

                json_string = json.dumps(chunk_dict)
                yield f"{json_string}\n".encode('utf-8') # Yield JSON string + newline, encoded
            except Exception as e:
                # Log error or yield an error message if conversion fails
                error_message = json.dumps({"error": f"Failed to serialize chunk: {e}", "chunk_type": str(type(chunk))})
                yield f"{error_message}\n".encode('utf-8')

    return StreamingResponse(stream_agent_response_json(request.user_query), media_type="application/x-ndjson")


if __name__ == "__main__":
    uvicorn.run("fastapi_agent:app", host="127.0.0.1", port=8000, reload=True)
