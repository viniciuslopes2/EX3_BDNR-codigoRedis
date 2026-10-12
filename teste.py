import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://viniciuslopes-bdnr:root@cluster0.uqrhmgw.mongodb.net/?appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())

try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)