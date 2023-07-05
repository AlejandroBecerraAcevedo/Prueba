from fastapi import APIRouter, HTTPException, status,Depends,Body
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from app.services.user_service import UserService
from app.core.security import create_acces_token, create_refresh_token
from app.schemas.auth_schema import TokenPayload, TokenSchema
from app.schemas.user_schema import UserOut
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.core.config import settings
from jose import jwt
from datetime import datetime, timedelta
from pydantic import ValidationError



auth_router = APIRouter()


@auth_router.post('/login', summary="origina el acces and refresh token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_acces_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }
    # crear los tokens|
    
@auth_router.post('/test-token', summary="testeo de valides del token", response_model=UserOut)
async def test_token(user: User = Depends(get_current_user)) -> Any:    
    return user

@auth_router.post('/refresh', summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserService.get_user_by_id(token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
        )
    return {
        "access_token": create_acces_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
    }