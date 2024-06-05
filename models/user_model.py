
from sqlalchemy import Column, Integer, String

from core.config import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String)
    email: str = Column(String)
    hashed_pass: str = Column(String)