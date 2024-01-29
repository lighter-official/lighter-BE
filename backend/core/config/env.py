from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENV: str = 'prod'
    RELOAD: bool = False
    DB_URI: str
    KAKAO_CLIENT_ID: str
    KAKAO_CLIENT_SECRET_ID: str
    JWT_SECRET: str

    class Config:
        env_file = '.env'

env = Settings()