from fastapi import APIRouter
from pymongo import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

router = APIRouter()

@router.get("/")
def data():
    uri = ''

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client["gloo"]
    collection = db["sample"]
    data = collection.find_one()

    return data

