
from bson import ObjectId
from .database import DatabaseService


class ChatService(DatabaseService):
    def __init__(self):
        super().__init__()
    
    def create_chat(self, user_id, chat_title=""):
        # Create a new chat -> Create a document in the database with user_id and chat_title(optional)
        return self.add_document(collection='chats', document={'user_id': user_id, 'chat_title': chat_title})
    
    def update_chat_title(self, chat_id, chat_title):
        # Update the chat_title of the chat
        return self.update_document(collection='chats', document={'_id': ObjectId(chat_id)}, extra={'$set' : {'chat_title': chat_title}})

    def get_conversations(self, chat_id, limit=100):
        # Get the conversation from the database
        # Maybe add a limit to the number of messages returned
        return self.get_documents(collection='conversations', document={'chat_id': ObjectId(chat_id)})
    
    def add_conversation(self, chat_id, conversation):
        # Add a conversation to the database
        return self.upsert_document(
            collection='conversations',
            document={'chat_id': ObjectId(chat_id)}, 
            extra={'$push': {'content': conversation}}
        )
    
    def delete_chat(self, chat_id):
        # Delete the chat from the database
        return self.delete_document(collection='chats', document={'_id': ObjectId(chat_id)})

    def check_if_chat_id_exists(self, chat_id):
        # Check if the chat_id exists in the database
        return self.get_document(collection='chats', document={'_id': ObjectId(chat_id)})