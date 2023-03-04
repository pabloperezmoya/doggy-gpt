from cgi import test
from pydoc import doc
from turtle import back
from typing import Dict, List
from fastapi import APIRouter, Body, Path, BackgroundTasks
from fastapi.responses import StreamingResponse
from requests import Response

from services.chat_service import ChatService

from services.openai_service import Openai_CompletionStream
from services.openai_service import Openai_Completion

import json
router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("/get_conversations/{chat_id}")
async def get_conversations(chat_id: str = Path(...)):
    # Get the conversation from the database
    # conversation: List[Dict] = DatabaseService.get_conversation(chat_id).content
    service = ChatService()

    conversation_document_cursor = service.get_conversations(chat_id)
    # return conversation
    def json_generator():
      for document in conversation_document_cursor:
          document['_id'] = str(document['_id'])
          document['chat_id'] = str(document['chat_id'])
          yield json.dumps(document).encode('utf-8')
  
    # Devolver el resultado como un StreamingResponse
    return StreamingResponse(json_generator(), media_type="application/json")

# Post: Get user input and return bot response
# Save it to the database

from pydantic import BaseModel

class UserMessage(BaseModel):
    role: str = "user"
    content: str


@router.post("/user_input/{chat_id}")
async def create_message_completion(background_tasks: BackgroundTasks, chat_id:str = Path(...), user_input:UserMessage = Body(...)):
    service = ChatService()
    
    # Check if the chat_id exists in the database
    if service.check_if_chat_id_exists(chat_id) == None:
        # If it doesn't, raise an error
        ...

    # If it does, get the conversation from the database

    # Getting the conversations from the database -> Returns a Cursor
    conversation_document = service.get_conversations(chat_id)
    
    try:
        conversations: List[Dict] = list(conversation_document)[0]['content'] # Get all content, isnt async so it should be ok
    except:
        conversations = []
    # Append the user_input to the conversation list -> conversation.append(user_message)
    user_input = user_input.dict() # Parsing user input to dict
    conversations.append(user_input) # Adding to conversations list, this is going to the openai service

    # Send the conversation to the OpenAI service -> Returns a Stream    
    responseStream = Openai_CompletionStream(conversations)

    content_raw: list = []
    content_clean: str = ''
    assistant_response = None
    
    def json_generator():
        idx = 0
        for chunk in responseStream:
          
          try:
              chunk.choices[0]['delta']['content']
              text = chunk.choices[0]['delta']['content']
              # print(text)
              content_raw.append(text)
              
              
              yield json.dumps({ 'part_id': idx, 'content': text }).encode('utf-8')
              idx += 1
          except:
              pass
          
        # ADDING HERE BECAUSE ITS THE LAST FUNCTION EXECUTED AND WHERE THE CONVERSATION IS COMPLETE
        # Saving the conversation to the database
        content_clean = "".join(content_raw)
        assistant_response = {'role': 'assistant', 'content': content_clean}
        background_tasks.add_task(conversations.append, assistant_response) # Adding to conversations list
        background_tasks.add_task(service.add_conversation, chat_id, user_input) # Adding user input to database
        background_tasks.add_task(service.add_conversation, chat_id, assistant_response) # Adding assistant response to database

        if len(conversations) == 5: # Generating title if conversation is 5 messages long
          background_tasks.add_task(generate_title, conversations, chat_id)

    # Devolver el resultado como un StreamingResponse
    return StreamingResponse(json_generator(), media_type="application/json")

def generate_title(conversations, chat_id):
    conversations.append({'role': 'user', 'content': 'Genera un titulo para esta conversación, no puede tener más de 50 caracters'})
    resp = dict(Openai_Completion(conversations))
    service = ChatService()
    service.update_chat_title(chat_id, resp['content'])


class ChatCreate(BaseModel):
    user_id: str
    chat_title: str = "Nuevo Chat"

@router.post("/create_chat")
async def create_chat(chat_create: ChatCreate = Body()):
    # Create a new chat -> Create a document in the database with user_id and chat_title(optional)
    # Return the _id of the document (as chat_id)
    # DatabaseService.create_chat(user_id, chat_title)
    user_id, chat_title = chat_create.user_id, chat_create.chat_title
    service = ChatService()
    try:
        chat_id = str(service.create_chat(user_id, chat_title).inserted_id)
    except:
        return "Error"
    
    return {"chat_id": chat_id}

@router.get("/get_chat/{user_id}")
async def get_chat(user_id: str = Path(...)):
    # Get the chat from the database
    # chat: List[Dict] = DatabaseService.get_chat(user_id).content
    service = ChatService()
    chat_document_cursor = service.get_chats(user_id)
    # return chat
    
    chat_list = []
    for document in chat_document_cursor:
      document['_id'] = str(document['_id'])
      document['user_id'] = str(document['user_id'])
      chat_list.append(document)

    return chat_list
