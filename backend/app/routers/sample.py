from fastapi import APIRouter
from pymongo import settings
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from backend.core.config.env import env
from backend.core.config.env import Settings
from backend.core.db.connect import sample_db

router = APIRouter()

@router.get("/")
def data():
    data = sample_db.find_one()

    return data

