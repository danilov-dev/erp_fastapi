from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.users.model import User
from app.users.schema import UserCreate
from app.shared.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, User)

    async def get_by_username(self, username: str) -> User:
        return await self.get_by_field(username=username)

    async def get_by_email(self, email: str) -> User:
        return await self.get_by_field(email=email)

    async def create(self, user_in: UserCreate) -> User:
        user_data = user_in.model_dump()  # TODO Реализовать хеширование пароля
        # user_data = user_in.model_dump(exclude={"password"})
        # hashed_password = get_password_hash(user_in.password)
        user = User(**user_data)
        self._async_session.add(user)
        await self._async_session.flush()
        await self._async_session.refresh(user)
        await self._async_session.commit()
        return user

    async def update_password(self, user_id: int, password: str) -> User:
        user = await self.get_by_id(user_id)
        user.password = password
        self._async_session.add(user)
        await self._async_session.flush()
        await self._async_session.refresh(user)
        return user

async def get_user_repository(
    session: AsyncSession = Depends(get_async_session)
) -> UserRepository:
    return UserRepository(session)