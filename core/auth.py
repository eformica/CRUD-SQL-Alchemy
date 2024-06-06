from pytz import timezone

from datetime import datetime, timedelta
from typing import List, Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from models.user_model import UserModel
from core.config import settings
from core.security import verificar_senha

from pydantic import EmailStr

oauth2schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login")

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        q = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(q)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None
        
        if not verificar_senha(senha, user.hashed_pass):
            return None
        
        return user

def _create_token(tipo_token: str, tempo_vida: int, sub: str) -> str:
    #https://datatracker.ietf.org/doc/rfc7519/
    
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub) #identificador do usuario

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def create_access_token(sub: str) -> str:
    #https://jwt.io/
    return _create_token(
        tipo_token = "access_token"
        , tempo_vida = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
        , sub = str(sub)
        )



