import os
import json
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def search_kb(question:str):
    "Load whole knowlledge from json file"
    
    with open("KB.json","rb") as f:
        return json.load(f)
    

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Search the knowledge base for a given question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"}
                },
                "required": ["question"],
                "additionalProperties": False  
            },
            "strict": True 
        }
    }
]
system_prompt = "You are a helpful assistant that can answer questions based on a knowledge base."

messages = [
    {
        "role": "system", "content": system_prompt
    },
    {
        "role": "user", "content": "What is Api"
    }
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

tool_call = completion.choices[0].message.tool_calls[0]

args = json.loads(tool_call.function.arguments)

result = search_kb(args["question"])

messages.append(completion.choices[0].message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

response = completion_2.choices[0].message.content

print(response)

# Structured response 

class KBResponse(BaseModel):
    answer : str = Field(description="The answer to the user's question from the knowledge base.")
    source : str = Field (description="The record id of the answer")
    
structured_completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=KBResponse
)

structured_response = structured_completion.choices[0].message.parsed

print(structured_response)