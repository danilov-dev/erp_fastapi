from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.users.model import User
from app.users.schema import UserRead, UserCreate
from app.users.service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_users(service: UserService = Depends(get_user_service)):
    return await service.get_all_users()

@router.post("/")
async def create_user(
    user_in: UserCreate, user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User could not be created"
        )
    return user



