from agno.agent import Agent

agent = Agent(
    instructions=["you can answer users question", "tell a joke"],
    description="You are a highly intelligent assistant.",
    add_datetime_to_instructions=True,
    context={"datetime": "Add current time to your response."},
    add_context=True,
    monitoring=True,
    markdown=True,
)
agent.print_response("what was my previous question", stream=True)