from fastapi import APIRouter
from pymongo import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from backend.core.config.env import env
from backend.core.config.env import Settings

uri = env.DB_URI

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["gloo"]
sample_db = db["sample"]
writing_setting_db = db["writing_setting"]
writing_db = db["writing"]
finished_writing_setting_db = db["finished_writing_setting"]
finished_writing_db = db["finished_writing"]
user_db = db["user"]
my_badge_db = db["my_badge"]
badges_db = db["badges"]
