
from google.cloud import firestore
from models import Item
import firebase_admin
from firebase_admin import credentials

class Database:

    def __init__(self):
        cred = credentials.Certificate("./serviceAccount.json")
        firebase_admin.initialize_app(cred)
        
        self.__db = firestore.Client()
        
    def get_collection(self, collection_name: 'translations' | 'users'):        
        return self.__db.collection(collection_name)
    
    def get_db(self):
        return self.__db



