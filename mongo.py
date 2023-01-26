from pymongo.collection import Collection
from config import client, database_name

class ChannelsDB:
    def __init__(self):
        self.files_col = Collection(client['Bot'], 'ChannelsDB')
        
    def find(self, data):
        return self.files_col.find_one(data)
    
    def full(self):
        return list(self.files_col.find())

    def add(self, data):
        try:
            self.files_col.insert_one(data)
        except:
            pass

    def remove(self, data):
        self.files_col.delete_one(data)

class UsersDB:
    def __init__(self):
        self.files_col = Collection(client['Bot'], database_name)
        
    def find(self, data):
        return self.files_col.find_one(data)
    
    def full(self):
        return list(self.files_col.find())

    def add(self, data):
        try:
            self.files_col.insert_one(data)
        except:
            pass

    def remove(self, data):
        self.files_col.delete_one(data)