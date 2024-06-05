from pydantic_settings import BaseSettings

from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://fast_api_test:qwert123@localhost:5432/fast_api_test"
    DBBaseModel: object = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()