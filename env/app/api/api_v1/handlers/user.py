from fastapi import APIRouter,HTTPException,status
from beanie.exceptions import RevisionIdWasChanged
from app.schemas.user_schema import UserAuth, UserOut
from app.services.user_service import UserService

from pymongo import errors


user_router = APIRouter()

@user_router.post('/create', summary="Create new user",response_model=UserOut)
async def create_user(data: UserAuth):
    try:        
        return await UserService.create_user(data)
    except (errors.DuplicateKeyError, RevisionIdWasChanged):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )