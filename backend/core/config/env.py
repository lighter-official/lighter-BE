from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = 'dev'

    class Config:
        env_file = '.env'


