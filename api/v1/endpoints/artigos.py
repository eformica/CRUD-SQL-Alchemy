from typing import List
from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel

from models.artigos_model import ArtigoModel
from schemas.artigo_schema import ArtigoSchema

from core.deps import get_session, get_current_user

router = APIRouter()

#POST
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    new = ArtigoModel(titulo = artigo.titulo, user_id = usuario_logado.id)

    db.add(new)

    await db.commit()

    return new

#GET
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(ArtigoModel)
        result = await session.execute(q)
        artigo = result.unique().scalars().all()

        return artigo

@router.get("/{id_artigo}", status_code=status.HTTP_200_OK, response_model=ArtigoSchema)
async def get_artigo_by_id(id_artigo: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(ArtigoModel).filter(ArtigoModel.id_artigo==id_artigo)
        result = await session.execute(q)
        artigo = result.unique().scalars().one_or_none()

        if artigo:
            return artigo
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found.")

#PUT
@router.put("/{id_artigo}", status_code=status.HTTP_202_ACCEPTED, response_model=ArtigoSchema)
async def put_artigo(id_artigo: int, artigo_update: ArtigoSchema, usuario_logado: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(ArtigoModel).filter(ArtigoModel.id_artigo==id_artigo)
        result = await session.execute(q)
        artigo = result.unique().scalars().one_or_none()

        if artigo:
            if artigo.titulo:
                artigo.titulo = artigo_update.titulo

            await session.commit()

            return artigo
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "Not found.")
        
#DELETE
@router.delete("/{id_artigo}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_artigo: int, usuario_logado: UserModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(ArtigoModel).filter(ArtigoModel.id_artigo==id_artigo).filter(ArtigoModel.user_id==usuario_logado.id)
        result = await session.execute(q)
        artigo = result.unique().scalars().one_or_none()

        if artigo:
            await session.delete(artigo)
            await session.commit()
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "Not found.")
        
