from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["bi_automation_db"]
