from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchema
from core.deps import get_session

router = APIRouter()

#POST
@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_user(user: UserSchema, db: AsyncSession = Depends(get_session)):
    new_user = UserModel(name = user.name, email = user.email, hashed_pass = user.hashed_pass)

    db.add(new_user)

    await db.commit()

    return new_user

#GET
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel)
        result = await session.execute(q)
        users = result.scalars().all()

        return users

@router.get("/{id_user}", status_code=status.HTTP_200_OK)
async def get_user_by_id(id_user: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.scalars().one_or_none()

        if user:
            return user
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")

#PUT
@router.put("/{id_user}", status_code=status.HTTP_202_ACCEPTED)
async def put_user(id_user: int, user_update: UserSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.scalars().one_or_none()

        if user:
            user.name = user_update.name
            user.email = user_update.email
            user.hashed_pass = user_update.hashed_pass

            await session.commit()

            return user_update
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
        
#DELETE
@router.delete("/{id_user}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id_user: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        q = select(UserModel).filter(UserModel.id==id_user)
        result = await session.execute(q)
        user = result.scalars().one_or_none()

        if user:
            await session.delete(user)
            await session.commit()
        else:
            return HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
        
