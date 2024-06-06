
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from core.config import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_pass = Column(String, nullable=False)
    auth_admin = Column(Boolean, default=False)

    artigos = relationship("ArtigoModel", cascade="all, delete-orphan", back_populates="owner", uselist=True, lazy="joined")
