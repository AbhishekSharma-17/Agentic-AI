from agents import Agent , Runner , GuardrailFunctionOutput
from pydantic import BaseModel
import asyncio

class Homeworkoutput(BaseModel):
    is_homework : bool
    reasoning : str

guardrail_agent = Agent(
    name="Homework Guardrail Check",
    instructions="checkif the user's is asking about homework.",
    output_type=Homeworkoutput

)

science_agent = Agent(
    name="science Tutor",
    instructions="You provide assistance with scientific queries. Explain scientific concepts clearly and provide examples where applicable.",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(Homeworkoutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent, science_agent]
)
    
async def main():

    result = await Runner.run(triage_agent, "what is ")
    print(result.raw_responses)

if __name__ == "__main__":
        asyncio.run(main())