import os
import base64
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o")

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

response = chain.invoke({"image_data": image_data})
print(response.content)