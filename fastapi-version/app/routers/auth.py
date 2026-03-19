from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import Annotated
from app.database import get_session
from app.core.auth import create_access_token, get_current_user
from app.models import User
from app.schemas.auth import UserCreate, UserResponse, UserCreateResponse, LoginResponse

router = APIRouter()

DatabaseSession = Annotated[Session, Depends(get_session)]
UserAuthentication = Annotated[User, Depends(get_current_user)]

@router.post("/register", response_model=UserCreateResponse)
async def register_user(session: DatabaseSession, user_data: UserCreate):
    statement = select(User).where(User.username == user_data.username)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    
    new_user = User(username=user_data.username)
    new_user.set_password(user_data.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserCreateResponse(
        user=UserResponse(id=new_user.id, username=new_user.username),
        message="User created successfully",
    )

@router.post("/login", response_model=LoginResponse)
async def login(session: DatabaseSession, form_data: OAuth2PasswordRequestForm = Depends()):
    statement = select(User).where(User.username == form_data.username)
    user = session.exec(statement).first()

    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(username=user.username)
    return LoginResponse(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout(current_user: UserAuthentication):
    return {"message": "Successfully logged out"}