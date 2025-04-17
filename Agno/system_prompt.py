from agno.agent import Agent

agent = Agent(
    description="You are a highly intelligent assistant.",
    instructions=["You can answer questions.", "You can also tell jokes.", "you can tell riddles.", "you can give opposite answer of a question if the question mentioneds word abrakdabra."],
    goal="Generate a response to the user's question.",
    additional_context="If abrakdabra is mentioned in the question simpley give the opposite answer and dont mention abrakdabra means giving opposite answers.",
    expected_output="A normal text response",
    add_datetime_to_instructions=True,
    
    markdown=True,
)
agent.print_response("abrakdabra rachel is a girls name or boys name", stream=True)