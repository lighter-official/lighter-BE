import uvicorn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

class Settings(BaseSettings):
    APP_ENV: str = 'dev'
    DB_URL: str

    class Config:
        env_file = '.env'

if __name__ == "__main__":
    settings = Settings()
    print(f'env: {settings.APP_ENV}')
    uvicorn.run("application:app", host='0.0.0.0', port=8000, log_level="info", factory=True, reload=True)