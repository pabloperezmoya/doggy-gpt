import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def Openai_Completion(conversation):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= conversation,
        max_tokens=200,
        temperature=0.7,
        n=1
        
    )
    # usage = resp.usage.total_tokens
    return resp.choices[0].message

# conversation = []
# while True:
#     message = input("User: ")    
#     conversation.append({"role": "user", "content": message})

#     resp = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",
#       messages= conversation,
#       max_tokens=200,
#       temperature=0.7,
#       n=1
#     )
#     conversation.append(resp.choices[0].message)
#     print(resp.usage.total_tokens)
#     print(resp)

#     print("Bot: ", resp.choices[0].message.content)