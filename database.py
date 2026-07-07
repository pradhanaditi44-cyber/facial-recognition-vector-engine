from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["dementia_project"]

print("Connected successfully!")