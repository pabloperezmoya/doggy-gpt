
from bson import ObjectId
from .database import DatabaseService


class UserService(DatabaseService):
    def __init__(self):
        super().__init__()

    def create_user(self, token):
        # Create a new user -> Create a document in the database with username
        return self.add_document(collection='users', document={'token': token})

    def get_user(self, user_id):
        # Get the user from the database
        return self.get_document( collection='users', 
                                  document={'_id': ObjectId(user_id)})
    
    def get_user_by_short_id(self, short_id):
        # Get the user from the database
        return self.get_document( collection='users', 
                                  document={'short_id': ObjectId(short_id)})

    def update_user(self, user_id, token, short_id):
        # Update the token of the user
        return self.update_document(  collection='users', 
                                      document={'_id': ObjectId(user_id)}, 
                                      extra={'$set': {
                                                  'token': token, 
                                                  'short_id': ObjectId(short_id)}})    