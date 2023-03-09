import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def Openai_Completion(conversation):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=400,
        temperature=0.7,
        n=1
    )
    return resp.choices[0].message


def OpenAI_StreamCompletion(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=400,
        temperature=0.7,
        n=1,
        stream=True
    )
    return response
