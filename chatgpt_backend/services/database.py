import os
import pymongo

from dotenv import load_dotenv
load_dotenv()
mongo_constr = os.environ.get('MONGO_URI')

class DatabaseService:
    def __init__(self):
        self.client = pymongo.MongoClient(mongo_constr + "/?retryWrites=true&w=majority")
        self.db = self.client.get_database('floppy-gpt')
    
    def add_document(self, collection, document):
        return self.db[collection].insert_one(document)
    
    def update_document(self, collection, document, extra):
        return self.db[collection].update_one(document, extra)
    
    def get_document(self, collection, document):
        return self.db[collection].find_one(document)
    
    def get_documents(self, collection, document):
        return self.db[collection].find(document)
    
    def delete_document(self, collection, document):
        return self.db[collection].delete_one(document)
    
    def upsert_document(self, collection, document, extra):
        return self.db[collection].update_one(document, extra, upsert=True)