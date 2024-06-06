from typing import Optional, List

from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import ArtigoSchema

class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    auth_admin: bool = False

class UserSchemaUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    email: Optional[EmailStr]
    auth_admin: Optional[bool] = False
    senha: Optional[str]

class UserSchemaCreate(UserSchemaBase):
    senha: str

class UserSchemaArtigos(UserSchemaBase):
    artigos: Optional[List[ArtigoSchema]]