
from google.cloud import firestore
import firebase_admin

class Database:
    _instance = None

    def __init__(self):
        self.cred = firebase_admin.credentials.Certificate("serviceAccount.json")
        firebase_admin.initialize_app(self.cred)
        
        self.__db = firestore.Client()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
           
        
    def get_collection(self, collection_name: str):        
        return self.__db.collection(collection_name)
    
    def get_db(self):
        return self.__db


