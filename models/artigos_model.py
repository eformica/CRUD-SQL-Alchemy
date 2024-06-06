
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.config import settings

class ArtigoModel(settings.DBBaseModel):
    __tablename__ = "artigos"

    id_artigo = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("UserModel", back_populates="artigos", lazy="joined")

    hashed_pass: str = Column(String)
