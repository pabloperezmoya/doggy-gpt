from chatgpt_backend.services.chat_service import ChatService

chat_objectIds = []

def test_create_chat():
    chat_service = ChatService()
    chat_id = chat_service.create_chat(user_id='1234').inserted_id
    assert chat_id is not None
    chat_objectIds.append(chat_id)

def test_update_chat():
    chat_service = ChatService()
    chat_id = chat_service.create_chat(user_id='1234').inserted_id
    chat_title = 'Test Chat'
    chat_service.update_chat(chat_id=chat_id, chat_title=chat_title)
    chat = chat_service.get_document(collection='chats', document={'_id': chat_id})
    assert chat['chat_title'] == chat_title
    chat_objectIds.append(chat_id)


def test_add_conversation():
    chat_service = ChatService()
    # chat_id = chat_service.create_chat(user_id='1234').inserted_id
    chat_id = "64024bacdf208ae9405bd814"
    conversation = {'role': 'assistant', 'content': 'Python'}
    # {'role': 'asistant', 'content': 'Hello'},
    # {'role': 'user', 'content': 'How are you?'},
    # {'role': 'asistant', 'content': 'I am fine, thank you.'},
    # {'role': 'user', 'content': 'That is good to hear.'},
    # {'role': 'asistant', 'content': 'Yes, it is.'},
    # {'role': 'user', 'content': 'Bye'},
    # {'role': 'asistant', 'content': 'Bye'},
    
    chat_service.add_conversation(chat_id=chat_id, conversation=conversation)
    chat = chat_service.get_conversations(chat_id=chat_id)
    assert chat is not None


def test_get_conversations():
    chat_service = ChatService()
    chat_id = "64024bacdf208ae9405bd814"
    chat = chat_service.get_conversations(chat_id=chat_id)
    
    for i in chat:
        print(i)

    assert chat is not None

def test_delete():
    chat_service = ChatService()
    count = 0
    for obId in chat_objectIds:
        chat = chat_service.delete_chat(chat_id=obId).deleted_count
        count += chat
    
    assert count == len(chat_objectIds)