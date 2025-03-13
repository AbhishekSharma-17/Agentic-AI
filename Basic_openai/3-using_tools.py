import os
import  json
import requests
from openai import OpenAI
from pydantic import BaseModel,Field
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define functions or tools both same , that we will call

def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']


tools = [
    {
         "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    },
    
    }
]

system_prompt = "You are a helpful assistant that can provide current weather information based on geographical coordinates."
messages = [
    {
        "role": "system", "content": system_prompt
    },
    {
        "role": "user", "content": "What is the current weather in lonavla today" 
    }
    
    ]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

tool_call = completion.choices[0].message.tool_calls[0]

args = json.loads(tool_call.function.arguments)

result = get_weather(args["latitude"], args["longitude"])

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

# A structured response containing the current weather information

class weatherResponse(BaseModel):
    temperature: float = Field(description = "Current temperature in Celsius")
    wind_speed: float = Field(description = "Current wind speed in meters per second")
    humidity: float = Field(description = "Current relative humidity in percentage")
    response: str = Field(description="A natural language description of the weather conditions")
    
    
structured_completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=weatherResponse,
)

structured_response = structured_completion.choices[0].message.parsed

print(structured_response) 