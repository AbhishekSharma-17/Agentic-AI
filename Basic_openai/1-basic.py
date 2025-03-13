import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Invokation

completion = client.chat.completions.create(model="o3-mini-2025-01-31",
                                            messages=[
                                                {
                                                    "role":"system","content":"Provide helpful and accurate responses to user queries."
                                                },
                                                {
                                                    "role":"user","content":"What is the capital of France?"
                                                }
                                            ]
                                            )

response = completion.choices[0].message.content
print(response)

# Streaming 

completion = client.chat.completions.create(model="o3-mini-2025-01-31",
                                            messages=[
                                                {
                                                    "role":"system","content":"Provide helpful and accurate responses to user queries."
                                                },
                                                {
                                                    "role":"user","content":"What is the capital of France?"
                                                }
                                            ],
                                            stream=True,
                                            
                                            )

for chunk in completion:
    token = chunk.choices[0].delta.content
    if token is not None:
        print(token, end="", flush=True)

    