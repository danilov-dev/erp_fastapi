from typing import List

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.users.repository import UserRepository
from app.users.schema import UserRead, UserUpdate, UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_all_users(self) -> List[UserRead]:
        users = await self.repository.get_all()
        return [UserRead.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserRead:
        user_out = await self.repository.get_by_id(user_id)
        return UserRead.model_validate(user_out)

    async def get_by_username(self, username: str) -> UserRead:
        user_out = await self.repository.get_by_username(username)
        return UserRead.model_validate(user_out)

    async def get_by_email(self, user_email: str) -> UserRead:
        user_out = await self.repository.get_by_email(user_email)
        return UserRead.model_validate(user_out)

    async def update_user(self, user_id: int, user_in: UserUpdate) -> UserRead:
        user_out = self.repository.update(user_id, user_in)
        return UserRead.model_validate(user_out)

    async def delete_user(self, user_id: int):
        return await self.repository.delete(user_id)

    async def create_user(self, user_in: UserCreate) -> UserRead:
        user_out = await self.repository.create(user_in)
        return UserRead.model_validate(user_out)

    async def is_repeat(self, user_in: UserRead) -> bool:
        is_repeat = False
        check_name = await self.repository.get_by_username(user_in.username)
        check_email = await self.repository.get_by_email(str(user_in.email))
        if check_name or check_email:
            is_repeat = True
        return is_repeat

async def get_user_service(
        async_session: AsyncSession = Depends(get_async_session)
) -> UserService:
    repository = UserRepository(async_session)
    return UserService(repository)