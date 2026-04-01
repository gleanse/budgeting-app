from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import Annotated
from app.database import get_session
from app.core.auth_core import get_current_user
from app.models import User
from app.schemas.auth_schema import UserCreate, UserResponse, UserCreateResponse, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]

@router.post("/register", response_model=UserCreateResponse)
async def register_user(session: DatabaseSession, user_data: UserCreate):
    auth_service = AuthService(session)

    try:
        new_user = auth_service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return UserCreateResponse(
        user=UserResponse(id=new_user.id, username=new_user.username),
        message="User created successfully",
    )

@router.post("/login", response_model=LoginResponse)
async def login(session: DatabaseSession, form_data: OAuth2PasswordRequestForm = Depends()):
    auth_service = AuthService(session)
    
    try:
        access_token = auth_service.login(form_data.username, form_data.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return LoginResponse(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout(current_user: UserAuthentication):
    return {"message": "Successfully logged out"}