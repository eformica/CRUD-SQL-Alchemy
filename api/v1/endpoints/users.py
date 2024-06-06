from typing import List, Optional

from fastapi import APIRouter, HTTPException, status, Depends

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from fastapi.responses import JSONResponse

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArtigos

from core.security import gerar_hash_senha
from core.auth import autenticar, create_access_token
from core.deps import get_session, get_current_user

router = APIRouter()


#GET Logado
@router.get("/logado", response_model=UserSchemaBase)
def get_logado(usuario_logado: UserModel = Depends(get_current_user)):
    return usuario_logado

#POST (Signup)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(name = user.name
                         , email = user.email
                         , auth_admin = user.auth_admin
                         , hashed_pass = gerar_hash_senha(user.senha))

    try:
        db.add(new_user)

        await db.commit()

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= "Usuário já cadastrado.")

    return new_user

#GET
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel)
        result = await session.execute(q)
        users = result.unique().scalars().all()

        return users

@router.get("/{id_user}", status_code=status.HTTP_200_OK, response_model=UserSchemaArtigos)
async def get_user_by_id(id_user: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

#PUT
@router.put("/{id_user}", status_code=status.HTTP_202_ACCEPTED, response_model=UserSchemaBase)
async def put_user(id_user: int, user_update: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.unique().scalars().one_or_none()

        if user:
            if user_update.name:
                user.name = user_update.name
            if user_update.email:
                user.email = user_update.email
            if user_update.auth_admin:
                user.auth_admin = user_update.auth_admin
            if user_update.senha:
                user.hashed_pass = gerar_hash_senha(user_update.senha)

            await session.commit()

            return user
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
        
#DELETE
@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_user: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.unique().scalars().one_or_none()

        if user:
            await session.delete(user)
            await session.commit()
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
        
#Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Dados de acesso incorretos.")
    else:
        return JSONResponse(content={"access_token": create_access_token(user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
    
