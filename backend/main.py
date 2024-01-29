import uvicorn
from core.config.env import Settings, env
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

if __name__ == "__main__":
    print(f'env: {env.APP_ENV}')
    uvicorn.run("application:app", host='0.0.0.0', port=8000, log_level="info", factory=True, reload=env.RELOAD)