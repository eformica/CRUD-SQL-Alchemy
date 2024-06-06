from pydantic_settings import BaseSettings

from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://fast_api_test:qwert123@localhost:5432/fast_api_test"
    DBBaseModel: object = declarative_base()

    JWT_SECRET: str = 'K4W6pj8T3-VzfXviRyvN1yd_UT5SwPYxNw7en6jDZFg'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60*24*7

    class Config:
        case_sensitive = True

settings = Settings()