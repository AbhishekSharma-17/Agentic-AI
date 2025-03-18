import os
import base64
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="google/gemma-3-27b-it", api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",streaming=True)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "Openai_vision/tesco-shopping-receipt-CNTYDX.jpg"

image_data = encode_image(image_path)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Describe the image provided"),
        (
            "user",
            [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/jpeg;base64,{image_data}"},
                }
            ],
        ),
    ]
)

chain = prompt | model

response = chain.stream({"image_data": image_data})
for chunk in response:
    
    print(chunk.content,flush=True,end="")