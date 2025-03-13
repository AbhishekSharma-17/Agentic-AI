import os
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CalenderEvent(BaseModel):
    name : str
    date : str
    participation : list[str]
    
completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "extract event information"},
        {"role": "user", "content": "Create a calendar event for a team meeting on 2023-10-15 with participants Alice, Bob, and Charlie."}
    ],
    response_format=CalenderEvent,
)     
# It gives a structured json response
event = completion.choices[0].message.content
print(event)

# it parses the response

event  = completion.choices[0].message.parsed
print(event.name, event.date, event.participation)